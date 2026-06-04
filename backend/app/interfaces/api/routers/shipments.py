"""Shipment workflow API router."""

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response

from app.application.dto.shipment_dto import (
    CreateShipmentInput,
    DigitizedDataInput,
    ValidateShipmentInput,
)
from app.application.ports.shipment_repository import ShipmentRepository
from app.application.use_cases.approve_shipment import ApproveShipmentUseCase
from app.application.use_cases.client_approve import ClientApproveUseCase
from app.application.use_cases.compare_data import CompareDataUseCase
from app.application.use_cases.correct_data import CorrectDataUseCase
from app.application.use_cases.create_shipment import CreateShipmentUseCase
from app.application.use_cases.extract_pdf_data import ExtractPdfDataUseCase
from app.application.use_cases.finalize_shipment import FinalizeShipmentUseCase
from app.application.use_cases.get_pdf_file import GetPdfFileUseCase
from app.application.use_cases.get_shipment import GetShipmentUseCase
from app.application.use_cases.list_shipments import ListShipmentsUseCase
from app.application.use_cases.register_digitized_data import (
    RegisterDigitizedDataUseCase,
)
from app.application.use_cases.register_novelty import RegisterNoveltyUseCase
from app.application.use_cases.validate_and_transition import (
    ValidateAndTransitionUseCase,
)
from app.domain.entities.container import Container
from app.domain.entities.validation_result import ValidationResult
from app.domain.value_objects.shipment_status import ShipmentStatus
from app.infrastructure.storage.shipment_file_storage import ShipmentFileStorage
from app.interfaces.api.dependencies import (
    get_approve,
    get_compare,
    get_create_shipment,
    get_extract_pdf,
    get_shipment_repo,
    get_validate,
)
from app.interfaces.api.schemas.document import ComparisonResponseSchema
from app.interfaces.api.schemas.mappers import comparison_schema, document_data_schema
from app.interfaces.api.schemas.shipment import (
    DigitizedDataRequest,
    NoveltyRequest,
    ShipmentCreateRequest,
    ShipmentDetailResponse,
    ShipmentResponse,
    ValidateRequest,
    ValidateResponse,
)

router = APIRouter(prefix="/shipments", tags=["shipments"])


def _containers_from_request(raw: list[dict[str, str]]) -> list[Container]:
    return [
        Container(
            container_number=c.get("container_number", ""),
            seal=c.get("seal", ""),
            container_type=c.get("container_type", ""),
            packages=c.get("packages", ""),
            gross_weight_kgs=c.get("gross_weight_kgs", ""),
            measurement_cbm=c.get("measurement_cbm", ""),
        )
        for c in raw
    ]


@router.get("", response_model=list[ShipmentResponse])
async def list_shipments(
    status: ShipmentStatus | None = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    repo: ShipmentRepository = Depends(get_shipment_repo),
) -> list[ShipmentResponse]:
    """List shipments with optional status filter."""
    use_case = ListShipmentsUseCase(repo)
    items = await use_case.execute(status=status, skip=skip, limit=limit)
    return [
        ShipmentResponse(
            id=i.id,
            reference=i.reference,
            status=i.status.value,
            cargo_type=i.cargo_type,
            source_pdf_filename=i.source_pdf_filename,
            client_id=i.client_id,
            created_at=i.created_at,
        )
        for i in items
    ]


@router.post("", response_model=ShipmentResponse, status_code=201)
async def create_shipment(
    body: ShipmentCreateRequest,
    use_case: CreateShipmentUseCase = Depends(get_create_shipment),
    repo: ShipmentRepository = Depends(get_shipment_repo),
) -> ShipmentResponse:
    """Create shipment from an inbox PDF filename."""
    result = await use_case.execute(
        CreateShipmentInput(
            source_pdf_filename=body.source_pdf_filename,
            cargo_type=body.cargo_type,
            client_id=body.client_id,
            reference=body.reference,
        )
    )
    detail = await GetShipmentUseCase(repo).execute(result.shipment_id)
    return ShipmentResponse(
        id=detail.id,
        reference=detail.reference,
        status=detail.status.value,
        cargo_type=detail.cargo_type,
        source_pdf_filename=detail.source_pdf_filename,
        client_id=detail.client_id,
        created_at=detail.created_at,
    )


@router.get("/{shipment_id}", response_model=ShipmentDetailResponse)
async def get_shipment(
    shipment_id: UUID,
    repo: ShipmentRepository = Depends(get_shipment_repo),
) -> ShipmentDetailResponse:
    """Get shipment detail."""
    detail = await GetShipmentUseCase(repo).execute(shipment_id)
    return ShipmentDetailResponse(
        id=detail.id,
        reference=detail.reference,
        status=detail.status.value,
        cargo_type=detail.cargo_type,
        source_pdf_filename=detail.source_pdf_filename,
        client_id=detail.client_id,
        created_at=detail.created_at,
        novelty_description=detail.novelty_description,
        updated_at=detail.updated_at,
        extracted_data=(
            document_data_schema(detail.extracted_data)
            if detail.extracted_data is not None
            else None
        ),
    )


@router.post("/{shipment_id}/extract")
async def extract_pdf(
    shipment_id: UUID,
    use_case: ExtractPdfDataUseCase = Depends(get_extract_pdf),
) -> dict[str, object]:
    """Run PDF extraction pipeline."""
    data = await use_case.execute(shipment_id)
    return {"data": document_data_schema(data).model_dump()}


@router.get("/{shipment_id}/pdf")
async def get_pdf(
    shipment_id: UUID,
    repo: ShipmentRepository = Depends(get_shipment_repo),
) -> Response:
    """Stream original PDF for side-by-side viewer."""
    pdf_bytes, filename = await GetPdfFileUseCase(repo, ShipmentFileStorage()).execute(
        shipment_id
    )
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": 'inline; filename="document.pdf"',
            "Cache-Control": "private, max-age=3600",
        },
    )


@router.post("/{shipment_id}/digitized-data", status_code=204)
async def register_digitized(
    shipment_id: UUID,
    body: DigitizedDataRequest,
    repo: ShipmentRepository = Depends(get_shipment_repo),
) -> None:
    """Register operator-typed data."""
    await RegisterDigitizedDataUseCase(repo).execute(
        shipment_id,
        DigitizedDataInput(
            fields=body.fields,
            freight_terms=body.freight_terms,
            containers=_containers_from_request(body.containers),
            digitized_by=body.digitized_by,
        ),
    )


@router.get("/{shipment_id}/comparison", response_model=ComparisonResponseSchema)
async def get_comparison(
    shipment_id: UUID,
    use_case: CompareDataUseCase = Depends(get_compare),
) -> ComparisonResponseSchema:
    """Field-by-field diff for executive review."""
    output = await use_case.execute(shipment_id)
    return comparison_schema(
        str(shipment_id),
        ValidationResult(
            shipment_id=str(shipment_id),
            is_complete=output.is_complete,
            fields=output.fields,
        ),
    )


@router.patch("/{shipment_id}/digitized-data", status_code=204)
async def correct_digitized(
    shipment_id: UUID,
    body: DigitizedDataRequest,
    repo: ShipmentRepository = Depends(get_shipment_repo),
) -> None:
    """Correct digitized data after INCOMPLETO."""
    await CorrectDataUseCase(repo).execute(
        shipment_id,
        DigitizedDataInput(
            fields=body.fields,
            freight_terms=body.freight_terms,
            containers=_containers_from_request(body.containers),
            digitized_by=body.digitized_by,
        ),
    )


@router.post("/{shipment_id}/validate", response_model=ValidateResponse)
async def validate_shipment(
    shipment_id: UUID,
    body: ValidateRequest,
    use_case: ValidateAndTransitionUseCase = Depends(get_validate),
) -> ValidateResponse:
    """Executive validation -> INCOMPLETO | COMPLETO."""
    result = await use_case.execute(
        shipment_id,
        ValidateShipmentInput(mark_complete=body.mark_complete),
    )
    return ValidateResponse(
        shipment_id=result.shipment_id,
        new_status=result.new_status.value,
    )


@router.post("/{shipment_id}/approve", status_code=204)
async def approve_shipment(
    shipment_id: UUID,
    use_case: ApproveShipmentUseCase = Depends(get_approve),
) -> None:
    """Approve and notify client (COMPLETO -> NOTIFICADO)."""
    await use_case.execute(shipment_id)


@router.post("/{shipment_id}/client-approve", status_code=204)
async def client_approve(
    shipment_id: UUID,
    repo: ShipmentRepository = Depends(get_shipment_repo),
) -> None:
    """Client approval (NOTIFICADO -> APROBADO_CLIENTE)."""
    await ClientApproveUseCase(repo).execute(shipment_id)


@router.post("/{shipment_id}/finalize", status_code=204)
async def finalize_shipment(
    shipment_id: UUID,
    repo: ShipmentRepository = Depends(get_shipment_repo),
) -> None:
    """Finalize shipment (APROBADO_CLIENTE -> FINALIZADO)."""
    await FinalizeShipmentUseCase(repo).execute(shipment_id)


@router.post("/{shipment_id}/novelty", status_code=204)
async def register_novelty(
    shipment_id: UUID,
    body: NoveltyRequest,
    repo: ShipmentRepository = Depends(get_shipment_repo),
) -> None:
    """Register novelty (APROBADO_CLIENTE -> CON_NOVEDAD -> EN_VALIDACION)."""
    await RegisterNoveltyUseCase(repo).execute(shipment_id, body.description)

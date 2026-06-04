"""Shipment-related DTOs."""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from app.domain.entities.container import Container
from app.domain.entities.digitized_data import DigitizedData
from app.domain.entities.document_data import DocumentData
from app.domain.entities.validation_result import FieldComparison
from app.domain.value_objects.cargo_type import CargoType
from app.domain.value_objects.shipment_status import ShipmentStatus


@dataclass(frozen=True)
class InboxPdfDTO:
    """PDF file available in the inbox folder."""

    filename: str
    size_bytes: int


@dataclass(frozen=True)
class CreateShipmentInput:
    """Input for creating a shipment from an inbox PDF."""

    source_pdf_filename: str
    cargo_type: CargoType
    client_id: UUID
    reference: str | None = None


@dataclass(frozen=True)
class CreateShipmentOutput:
    """Output after creating a shipment."""

    shipment_id: UUID
    reference: str
    status: ShipmentStatus


@dataclass(frozen=True)
class ShipmentListItem:
    """Summary row for shipment list."""

    id: UUID
    reference: str
    status: ShipmentStatus
    cargo_type: CargoType
    source_pdf_filename: str
    client_id: UUID
    created_at: datetime


@dataclass(frozen=True)
class ShipmentDetailOutput:
    """Full shipment detail."""

    id: UUID
    reference: str
    status: ShipmentStatus
    cargo_type: CargoType
    source_pdf_filename: str
    client_id: UUID
    extracted_data: DocumentData | None
    digitized_data: DigitizedData | None
    novelty_description: str
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class DigitizedDataInput:
    """Operator-typed data registration input."""

    fields: dict[str, str]
    freight_terms: str | None = None
    containers: list[Container] = field(default_factory=list)
    digitized_by: str = "operator"


@dataclass(frozen=True)
class ComparisonOutput:
    """Field-by-field comparison for executive review."""

    shipment_id: UUID
    is_complete: bool
    fields: list[FieldComparison]


@dataclass(frozen=True)
class ValidateShipmentInput:
    """Executive validation decision."""

    mark_complete: bool


@dataclass(frozen=True)
class ValidateShipmentOutput:
    """Result of executive validation."""

    shipment_id: UUID
    new_status: ShipmentStatus


@dataclass(frozen=True)
class ApproveShipmentInput:
    """Executive approval to notify client."""

    pass

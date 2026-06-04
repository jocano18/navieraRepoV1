"""Mappers between ORM models and domain entities (DTO + Mapper pattern)."""

import json
from datetime import UTC, datetime
from uuid import UUID

from app.domain.entities.client import Client
from app.domain.entities.container import Container
from app.domain.entities.digitized_data import DigitizedData
from app.domain.entities.document_data import DocumentData
from app.domain.entities.shipment import Shipment
from app.domain.entities.validation_result import FieldComparison, ValidationResult
from app.domain.value_objects.cargo_type import CargoType
from app.domain.value_objects.extracted_field import ExtractedField
from app.domain.value_objects.field_source import FieldSource
from app.domain.value_objects.freight_terms import FreightTerms
from app.domain.value_objects.shipment_status import ShipmentStatus
from app.infrastructure.persistence.models import ClientModel, ShipmentModel


def _aware_utc(dt: datetime) -> datetime:
    """Normalize DB naive timestamps to timezone-aware UTC for the domain."""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=UTC)
    return dt.astimezone(UTC)


def _naive_utc(dt: datetime) -> datetime:
    """PostgreSQL TIMESTAMP WITHOUT TIME ZONE expects naive UTC values."""
    if dt.tzinfo is None:
        return dt
    return dt.astimezone(UTC).replace(tzinfo=None)


def _field_to_dict(field: ExtractedField) -> dict[str, str]:
    return {"value": field.value, "source": field.source.value}


def _field_from_dict(data: dict[str, str] | None) -> ExtractedField:
    if not data:
        return ExtractedField.not_found()
    return ExtractedField(
        value=data.get("value", ""),
        source=FieldSource(data.get("source", FieldSource.NOT_FOUND.value)),
    )


def document_data_to_json(data: DocumentData | None) -> str | None:
    """Serialize DocumentData to JSON string."""
    if data is None:
        return None
    payload: dict[str, object] = {
        "text_source": data.text_source.value,
        "freight_terms": data.freight_terms.value if data.freight_terms else None,
        "containers": [
            {
                "container_number": c.container_number,
                "seal": c.seal,
                "container_type": c.container_type,
                "packages": c.packages,
                "gross_weight_kgs": c.gross_weight_kgs,
                "measurement_cbm": c.measurement_cbm,
            }
            for c in data.containers
        ],
    }
    for name, field in data.scalar_fields().items():
        payload[name] = _field_to_dict(field)
    return json.dumps(payload)


def document_data_from_json(raw: str | None) -> DocumentData | None:
    """Deserialize DocumentData from JSON."""
    if not raw:
        return None
    payload = json.loads(raw)
    data = DocumentData(
        text_source=FieldSource(payload.get("text_source", FieldSource.NATIVE.value)),
    )
    for name in data.scalar_fields():
        setattr(data, name, _field_from_dict(payload.get(name)))
    ft = payload.get("freight_terms")
    data.freight_terms = FreightTerms(ft) if ft else None
    data.containers = [Container(**c) for c in payload.get("containers", [])]
    return data


def digitized_data_to_json(data: DigitizedData | None) -> str | None:
    if data is None:
        return None
    return json.dumps(
        {
            **data.scalar_fields(),
            "freight_terms": data.freight_terms.value if data.freight_terms else None,
            "containers": [
                {
                    "container_number": c.container_number,
                    "seal": c.seal,
                    "container_type": c.container_type,
                    "packages": c.packages,
                    "gross_weight_kgs": c.gross_weight_kgs,
                    "measurement_cbm": c.measurement_cbm,
                }
                for c in data.containers
            ],
            "digitized_by": data.digitized_by,
        }
    )


def digitized_data_from_json(raw: str | None) -> DigitizedData | None:
    if not raw:
        return None
    payload = json.loads(raw)
    ft = payload.get("freight_terms")
    return DigitizedData(
        bl_number=payload.get("bl_number", ""),
        carrier_name=payload.get("carrier_name", ""),
        shipper=payload.get("shipper", ""),
        consignee=payload.get("consignee", ""),
        notify_party=payload.get("notify_party", ""),
        delivery_agent=payload.get("delivery_agent", ""),
        vessel_and_voyage=payload.get("vessel_and_voyage", ""),
        place_of_receipt=payload.get("place_of_receipt", ""),
        port_of_loading=payload.get("port_of_loading", ""),
        port_of_discharge=payload.get("port_of_discharge", ""),
        place_of_delivery=payload.get("place_of_delivery", ""),
        marks_and_numbers=payload.get("marks_and_numbers", ""),
        description_of_goods=payload.get("description_of_goods", ""),
        number_of_packages=payload.get("number_of_packages", ""),
        gross_weight_kgs=payload.get("gross_weight_kgs", ""),
        measurement_cbm=payload.get("measurement_cbm", ""),
        number_of_originals=payload.get("number_of_originals", ""),
        shipped_on_board_date=payload.get("shipped_on_board_date", ""),
        freight_terms=FreightTerms(ft) if ft else None,
        containers=[Container(**c) for c in payload.get("containers", [])],
        digitized_by=payload.get("digitized_by", ""),
    )


def validation_to_json(result: ValidationResult | None) -> str | None:
    if result is None:
        return None
    return json.dumps(
        {
            "shipment_id": result.shipment_id,
            "is_complete": result.is_complete,
            "fields": [
                {
                    "field": f.field,
                    "extracted_value": f.extracted_value,
                    "typed_value": f.typed_value,
                    "matches": f.matches,
                    "source": f.source.value,
                }
                for f in result.fields
            ],
        }
    )


def validation_from_json(raw: str | None) -> ValidationResult | None:
    if not raw:
        return None
    payload = json.loads(raw)
    return ValidationResult(
        shipment_id=payload["shipment_id"],
        is_complete=payload["is_complete"],
        fields=[
            FieldComparison(
                field=f["field"],
                extracted_value=f["extracted_value"],
                typed_value=f["typed_value"],
                matches=f["matches"],
                source=FieldSource(f["source"]),
            )
            for f in payload.get("fields", [])
        ],
    )


def shipment_to_domain(model: ShipmentModel) -> Shipment:
    """Map ORM model to domain Shipment aggregate."""
    return Shipment(
        id=UUID(model.id),
        reference=model.reference,
        source_pdf_filename=model.source_pdf_filename,
        cargo_type=CargoType(model.cargo_type),
        status=ShipmentStatus(model.status),
        client_id=UUID(model.client_id),
        extracted_data=document_data_from_json(model.extracted_data_json),
        digitized_data=digitized_data_from_json(model.digitized_data_json),
        validation_result=validation_from_json(model.validation_result_json),
        novelty_description=model.novelty_description or "",
        created_at=_aware_utc(model.created_at),
        updated_at=_aware_utc(model.updated_at),
    )


def shipment_to_model(
    shipment: Shipment, existing: ShipmentModel | None = None
) -> ShipmentModel:
    """Map domain Shipment to ORM model."""
    if existing:
        model = existing
    else:
        model = ShipmentModel(
            id=str(shipment.id),
            created_at=_naive_utc(shipment.created_at),
        )
    model.reference = shipment.reference
    model.source_pdf_filename = shipment.source_pdf_filename
    model.cargo_type = shipment.cargo_type.value
    model.status = shipment.status.value
    model.client_id = str(shipment.client_id)
    model.extracted_data_json = document_data_to_json(shipment.extracted_data)
    model.digitized_data_json = digitized_data_to_json(shipment.digitized_data)
    model.validation_result_json = validation_to_json(shipment.validation_result)
    model.novelty_description = shipment.novelty_description
    model.updated_at = _naive_utc(datetime.now(UTC))
    return model


def client_to_domain(model: ClientModel) -> Client:
    """Map ORM client to domain entity."""
    return Client(
        id=UUID(model.id),
        name=model.name,
        nit=model.nit,
        email=model.email,
        is_active=model.is_active,
    )


def client_to_model(client: Client) -> ClientModel:
    """Map domain client to ORM model."""
    return ClientModel(
        id=str(client.id),
        name=client.name,
        nit=client.nit,
        email=client.email,
        is_active=client.is_active,
    )

"""Shipment API schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.domain.value_objects.cargo_type import CargoType
from app.interfaces.api.schemas.document import DocumentDataSchema


class InboxPdfResponse(BaseModel):
    """Inbox PDF listing item."""

    filename: str
    size_bytes: int


class ShipmentCreateRequest(BaseModel):
    """Create shipment from inbox PDF."""

    source_pdf_filename: str
    cargo_type: CargoType
    client_id: UUID
    reference: str | None = None


class ShipmentResponse(BaseModel):
    """Shipment summary response."""

    id: UUID
    reference: str
    status: str
    cargo_type: CargoType
    source_pdf_filename: str
    client_id: UUID
    created_at: datetime


class ShipmentDetailResponse(ShipmentResponse):
    """Shipment detail with nested data."""

    novelty_description: str = ""
    updated_at: datetime
    extracted_data: DocumentDataSchema | None = None


class DigitizedDataRequest(BaseModel):
    """Operator-typed B/L fields."""

    fields: dict[str, str] = Field(default_factory=dict)
    freight_terms: str | None = None
    containers: list[dict[str, str]] = Field(default_factory=list)
    digitized_by: str = "operator"


class ValidateRequest(BaseModel):
    """Executive validation request."""

    mark_complete: bool = True


class ValidateResponse(BaseModel):
    """Validation result status."""

    shipment_id: UUID
    new_status: str


class NoveltyRequest(BaseModel):
    """Novelty registration."""

    description: str

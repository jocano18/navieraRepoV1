"""Pydantic schemas for document data (API layer — separate from domain)."""

from pydantic import BaseModel, Field


class ExtractedFieldSchema(BaseModel):
    """Extracted field with source/confidence."""

    value: str
    source: str


class ContainerSchema(BaseModel):
    """Container line schema."""

    container_number: str = ""
    seal: str = ""
    container_type: str = ""
    packages: str = ""
    gross_weight_kgs: str = ""
    measurement_cbm: str = ""


class DocumentDataSchema(BaseModel):
    """Extracted B/L document data response."""

    bl_number: ExtractedFieldSchema
    carrier_name: ExtractedFieldSchema
    shipper: ExtractedFieldSchema
    consignee: ExtractedFieldSchema
    notify_party: ExtractedFieldSchema
    delivery_agent: ExtractedFieldSchema
    vessel_and_voyage: ExtractedFieldSchema
    place_of_receipt: ExtractedFieldSchema
    port_of_loading: ExtractedFieldSchema
    port_of_discharge: ExtractedFieldSchema
    place_of_delivery: ExtractedFieldSchema
    marks_and_numbers: ExtractedFieldSchema
    description_of_goods: ExtractedFieldSchema
    number_of_packages: ExtractedFieldSchema
    gross_weight_kgs: ExtractedFieldSchema
    measurement_cbm: ExtractedFieldSchema
    number_of_originals: ExtractedFieldSchema
    shipped_on_board_date: ExtractedFieldSchema
    freight_terms: str | None = None
    containers: list[ContainerSchema] = Field(default_factory=list)
    text_source: str = "NATIVE"


class FieldComparisonSchema(BaseModel):
    """Single field comparison row."""

    field: str
    extracted_value: str
    typed_value: str
    matches: bool
    source: str


class ComparisonResponseSchema(BaseModel):
    """Comparison endpoint response."""

    shipment_id: str
    is_complete: bool
    fields: list[FieldComparisonSchema]

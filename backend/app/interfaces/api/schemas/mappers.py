"""API schema mappers (domain/ORM -> Pydantic)."""

from app.domain.entities.document_data import DocumentData
from app.domain.entities.validation_result import FieldComparison, ValidationResult
from app.domain.value_objects.extracted_field import ExtractedField
from app.interfaces.api.schemas.document import (
    ComparisonResponseSchema,
    ContainerSchema,
    DocumentDataSchema,
    ExtractedFieldSchema,
    FieldComparisonSchema,
)


def extracted_field_schema(field: ExtractedField) -> ExtractedFieldSchema:
    """Map domain ExtractedField to API schema."""
    return ExtractedFieldSchema(value=field.value, source=field.source.value)


def document_data_schema(data: DocumentData) -> DocumentDataSchema:
    """Map domain DocumentData to API schema."""
    return DocumentDataSchema(
        bl_number=extracted_field_schema(data.bl_number),
        carrier_name=extracted_field_schema(data.carrier_name),
        shipper=extracted_field_schema(data.shipper),
        consignee=extracted_field_schema(data.consignee),
        notify_party=extracted_field_schema(data.notify_party),
        delivery_agent=extracted_field_schema(data.delivery_agent),
        vessel_and_voyage=extracted_field_schema(data.vessel_and_voyage),
        place_of_receipt=extracted_field_schema(data.place_of_receipt),
        port_of_loading=extracted_field_schema(data.port_of_loading),
        port_of_discharge=extracted_field_schema(data.port_of_discharge),
        place_of_delivery=extracted_field_schema(data.place_of_delivery),
        marks_and_numbers=extracted_field_schema(data.marks_and_numbers),
        description_of_goods=extracted_field_schema(data.description_of_goods),
        number_of_packages=extracted_field_schema(data.number_of_packages),
        gross_weight_kgs=extracted_field_schema(data.gross_weight_kgs),
        measurement_cbm=extracted_field_schema(data.measurement_cbm),
        number_of_originals=extracted_field_schema(data.number_of_originals),
        shipped_on_board_date=extracted_field_schema(data.shipped_on_board_date),
        freight_terms=data.freight_terms.value if data.freight_terms else None,
        containers=[
            ContainerSchema(
                container_number=c.container_number,
                seal=c.seal,
                container_type=c.container_type,
                packages=c.packages,
                gross_weight_kgs=c.gross_weight_kgs,
                measurement_cbm=c.measurement_cbm,
            )
            for c in data.containers
        ],
        text_source=data.text_source.value,
    )


def comparison_schema(
    shipment_id: str,
    result: ValidationResult,
) -> ComparisonResponseSchema:
    """Map ValidationResult to API schema."""

    def row(field: FieldComparison) -> FieldComparisonSchema:
        return FieldComparisonSchema(
            field=field.field,
            extracted_value=field.extracted_value,
            typed_value=field.typed_value,
            matches=field.matches,
            source=field.source.value,
        )

    return ComparisonResponseSchema(
        shipment_id=shipment_id,
        is_complete=result.is_complete,
        fields=[row(f) for f in result.fields],
    )

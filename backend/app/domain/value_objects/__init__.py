"""Domain value objects."""

from app.domain.value_objects.bl_number import BlNumber
from app.domain.value_objects.cargo_type import CargoType
from app.domain.value_objects.extracted_field import ExtractedField
from app.domain.value_objects.field_source import FieldSource
from app.domain.value_objects.freight_terms import FreightTerms
from app.domain.value_objects.shipment_status import ShipmentStatus

__all__ = [
    "BlNumber",
    "CargoType",
    "ExtractedField",
    "FieldSource",
    "FreightTerms",
    "ShipmentStatus",
]

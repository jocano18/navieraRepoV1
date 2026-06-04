"""Document data entity — canonical B/L fields extracted from PDF."""

from dataclasses import dataclass, field

from app.domain.entities.container import Container
from app.domain.value_objects.extracted_field import ExtractedField
from app.domain.value_objects.field_source import FieldSource
from app.domain.value_objects.freight_terms import FreightTerms


@dataclass
class DocumentData:
    """Structured Bill of Lading data extracted from a PDF.

    Each scalar field is an ExtractedField carrying value + source (NATIVE/OCR).
    Mandatory field: bl_number (validated at extraction time).
    """

    bl_number: ExtractedField = field(default_factory=ExtractedField.not_found)
    carrier_name: ExtractedField = field(default_factory=ExtractedField.not_found)
    shipper: ExtractedField = field(default_factory=ExtractedField.not_found)
    consignee: ExtractedField = field(default_factory=ExtractedField.not_found)
    notify_party: ExtractedField = field(default_factory=ExtractedField.not_found)
    delivery_agent: ExtractedField = field(default_factory=ExtractedField.not_found)
    vessel_and_voyage: ExtractedField = field(default_factory=ExtractedField.not_found)
    place_of_receipt: ExtractedField = field(default_factory=ExtractedField.not_found)
    port_of_loading: ExtractedField = field(default_factory=ExtractedField.not_found)
    port_of_discharge: ExtractedField = field(default_factory=ExtractedField.not_found)
    place_of_delivery: ExtractedField = field(default_factory=ExtractedField.not_found)
    marks_and_numbers: ExtractedField = field(default_factory=ExtractedField.not_found)
    description_of_goods: ExtractedField = field(
        default_factory=ExtractedField.not_found
    )
    number_of_packages: ExtractedField = field(default_factory=ExtractedField.not_found)
    gross_weight_kgs: ExtractedField = field(default_factory=ExtractedField.not_found)
    measurement_cbm: ExtractedField = field(default_factory=ExtractedField.not_found)
    number_of_originals: ExtractedField = field(
        default_factory=ExtractedField.not_found
    )
    shipped_on_board_date: ExtractedField = field(
        default_factory=ExtractedField.not_found
    )
    freight_terms: FreightTerms | None = None
    containers: list[Container] = field(default_factory=list)
    text_source: FieldSource = FieldSource.NATIVE

    def scalar_fields(self) -> dict[str, ExtractedField]:
        """Return all scalar extracted fields as a name-to-field mapping."""
        return {
            "bl_number": self.bl_number,
            "carrier_name": self.carrier_name,
            "shipper": self.shipper,
            "consignee": self.consignee,
            "notify_party": self.notify_party,
            "delivery_agent": self.delivery_agent,
            "vessel_and_voyage": self.vessel_and_voyage,
            "place_of_receipt": self.place_of_receipt,
            "port_of_loading": self.port_of_loading,
            "port_of_discharge": self.port_of_discharge,
            "place_of_delivery": self.place_of_delivery,
            "marks_and_numbers": self.marks_and_numbers,
            "description_of_goods": self.description_of_goods,
            "number_of_packages": self.number_of_packages,
            "gross_weight_kgs": self.gross_weight_kgs,
            "measurement_cbm": self.measurement_cbm,
            "number_of_originals": self.number_of_originals,
            "shipped_on_board_date": self.shipped_on_board_date,
        }

    def has_mandatory_fields(self) -> bool:
        """Check whether bl_number was successfully extracted."""
        return self.bl_number.source != FieldSource.NOT_FOUND and bool(
            self.bl_number.value
        )

"""Digitized data — operator-typed mirror of DocumentData."""

from dataclasses import dataclass, field

from app.domain.entities.container import Container
from app.domain.value_objects.freight_terms import FreightTerms


@dataclass
class DigitizedData:
    """Manually typed B/L data entered by an operator for comparison."""

    bl_number: str = ""
    carrier_name: str = ""
    shipper: str = ""
    consignee: str = ""
    notify_party: str = ""
    delivery_agent: str = ""
    vessel_and_voyage: str = ""
    place_of_receipt: str = ""
    port_of_loading: str = ""
    port_of_discharge: str = ""
    place_of_delivery: str = ""
    marks_and_numbers: str = ""
    description_of_goods: str = ""
    number_of_packages: str = ""
    gross_weight_kgs: str = ""
    measurement_cbm: str = ""
    number_of_originals: str = ""
    shipped_on_board_date: str = ""
    freight_terms: FreightTerms | None = None
    containers: list[Container] = field(default_factory=list)
    digitized_by: str = ""

    def scalar_fields(self) -> dict[str, str]:
        """Return scalar fields as plain strings for comparison."""
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

    @classmethod
    def empty(cls) -> "DigitizedData":
        """Create an empty digitized data instance."""
        return cls()

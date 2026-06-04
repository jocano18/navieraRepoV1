"""Internal mappers between DTOs and domain entities (application layer only)."""

from app.application.dto.shipment_dto import (
    DigitizedDataInput,
    ShipmentDetailOutput,
    ShipmentListItem,
)
from app.domain.entities.digitized_data import DigitizedData
from app.domain.entities.shipment import Shipment
from app.domain.value_objects.freight_terms import FreightTerms


def digitized_from_input(data: DigitizedDataInput) -> DigitizedData:
    """Map DigitizedDataInput DTO to domain DigitizedData."""
    freight = FreightTerms.from_text(data.freight_terms) if data.freight_terms else None
    return DigitizedData(
        bl_number=data.fields.get("bl_number", ""),
        carrier_name=data.fields.get("carrier_name", ""),
        shipper=data.fields.get("shipper", ""),
        consignee=data.fields.get("consignee", ""),
        notify_party=data.fields.get("notify_party", ""),
        delivery_agent=data.fields.get("delivery_agent", ""),
        vessel_and_voyage=data.fields.get("vessel_and_voyage", ""),
        place_of_receipt=data.fields.get("place_of_receipt", ""),
        port_of_loading=data.fields.get("port_of_loading", ""),
        port_of_discharge=data.fields.get("port_of_discharge", ""),
        place_of_delivery=data.fields.get("place_of_delivery", ""),
        marks_and_numbers=data.fields.get("marks_and_numbers", ""),
        description_of_goods=data.fields.get("description_of_goods", ""),
        number_of_packages=data.fields.get("number_of_packages", ""),
        gross_weight_kgs=data.fields.get("gross_weight_kgs", ""),
        measurement_cbm=data.fields.get("measurement_cbm", ""),
        number_of_originals=data.fields.get("number_of_originals", ""),
        shipped_on_board_date=data.fields.get("shipped_on_board_date", ""),
        freight_terms=freight,
        containers=list(data.containers),
        digitized_by=data.digitized_by,
    )


def shipment_to_detail(shipment: Shipment) -> ShipmentDetailOutput:
    """Map Shipment aggregate to detail DTO."""
    return ShipmentDetailOutput(
        id=shipment.id,
        reference=shipment.reference,
        status=shipment.status,
        cargo_type=shipment.cargo_type,
        source_pdf_filename=shipment.source_pdf_filename,
        client_id=shipment.client_id,
        extracted_data=shipment.extracted_data,
        digitized_data=shipment.digitized_data,
        novelty_description=shipment.novelty_description,
        created_at=shipment.created_at,
        updated_at=shipment.updated_at,
    )


def shipment_to_list_item(shipment: Shipment) -> ShipmentListItem:
    """Map Shipment to list item DTO."""
    return ShipmentListItem(
        id=shipment.id,
        reference=shipment.reference,
        status=shipment.status,
        cargo_type=shipment.cargo_type,
        source_pdf_filename=shipment.source_pdf_filename,
        client_id=shipment.client_id,
        created_at=shipment.created_at,
    )

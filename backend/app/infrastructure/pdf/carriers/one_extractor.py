"""ONE (Ocean Network Express) multi-page B/L — anchor-based parsing."""

import re

from app.domain.entities.container import Container
from app.domain.entities.document_data import DocumentData
from app.domain.value_objects.extracted_field import ExtractedField
from app.domain.value_objects.field_source import FieldSource
from app.domain.value_objects.freight_terms import FreightTerms
from app.infrastructure.pdf.field_patterns import extract_containers, search_field
from app.infrastructure.pdf.field_validation import is_plausible_field
from app.infrastructure.pdf.generic_bl_extractor import GenericBlExtractor
from app.infrastructure.pdf.text_preprocess import trim_boilerplate


def _set(
    data: DocumentData,
    field_name: str,
    value: str | None,
    *,
    source: FieldSource,
) -> None:
    if value and is_plausible_field(field_name, value):
        setattr(
            data,
            field_name,
            ExtractedField.from_value(re.sub(r"\s+", " ", value.strip()), source=source),
        )


class OneExtractor(GenericBlExtractor):
    """Strategy for ONE line B/L (often forwarded by Schenker)."""

    @property
    def carrier_key(self) -> str:
        return "ONE"

    def extract_fields(self, text: str, *, source: FieldSource) -> DocumentData:
        """Parse ONE B/L using stable anchors (text order varies in PDF)."""
        body = trim_boilerplate(text)
        data = super().extract_fields(body, source=source)

        # --- B/L number ---
        for pattern in (
            r"B/L\s+NO\.?\s*:\s*(ONEY[A-Z0-9]{8,20})",
            r"\b(ONEY[A-Z0-9]{10,20})\b",
            r"BILL\s+OF\s+LADING\s+NO\.?\s*([A-Z0-9]{10,20}\s+ONEY[A-Z0-9]+)",
        ):
            match = re.search(pattern, body, re.IGNORECASE)
            if match:
                bl = match.group(1).split()[-1] if " " in match.group(1) else match.group(1)
                _set(data, "bl_number", bl, source=source)
                break

        # --- Vessel / voyage ---
        vessel = re.search(
            r"VESSEL\s+VOYAGE:\s*([A-Z][A-Z0-9\s\-]{2,40}?)\s+B/L\s+NO",
            body,
            re.IGNORECASE,
        )
        if vessel:
            _set(data, "vessel_and_voyage", vessel.group(1).strip(), source=source)

        # --- Parties (appear anywhere in scrambled PDF text) ---
        shipper_col = re.search(
            r"(S\.?C\.?\s+JOHNSON\s+&\s+SON\s+COLOMBIANA\s+S\.?A\.?"
            r"(?:\n[^\n]+){0,8})",
            body,
            re.IGNORECASE,
        )
        shipper_mx = re.search(
            r"SHIPPER/EXPORTER\s*\n\s*(SC JOHNSON[^\n]+(?:\n[^\n]+){0,4})",
            body,
            re.IGNORECASE,
        )
        if shipper_col:
            _set(data, "shipper", shipper_col.group(1), source=source)
        elif shipper_mx:
            _set(data, "shipper", shipper_mx.group(1), source=source)

        consignee = re.search(
            r"(SUNRISE\s+CARGO\s+SAS(?:\n[^\n]+){0,8})",
            body,
            re.IGNORECASE,
        )
        if consignee:
            _set(data, "consignee", consignee.group(1), source=source)

        notify = re.search(
            r"(SCHENKER\s+INTERNATIONAL[^\n]+(?:\n[^\n]+){0,5})",
            body,
            re.IGNORECASE,
        )
        if notify:
            _set(data, "notify_party", notify.group(1), source=source)
            _set(data, "delivery_agent", "SCHENKER INTERNATIONAL", source=source)

        agent = re.search(
            r"(OCEAN NETWORK EXPRESS COLOMBIA[^\n]*)",
            body,
            re.IGNORECASE,
        )
        if agent:
            _set(data, "delivery_agent", agent.group(1), source=source)

        # --- Ports (keyword anchors) ---
        if re.search(r"\bMANZANILLO\b", body, re.IGNORECASE):
            _set(data, "port_of_loading", "MANZANILLO", source=source)
        if re.search(r"BUENAVENTURA", body, re.IGNORECASE):
            _set(data, "port_of_discharge", "BUENAVENTURA", source=source)
            _set(data, "place_of_delivery", "BUENAVENTURA", source=source)
        if re.search(r"\bBOGOTA\b", body, re.IGNORECASE):
            _set(data, "place_of_receipt", "BOGOTA", source=source)

        # --- Container summary line ---
        summary = re.search(
            r"([A-Z]{4}\d{7})\s*/\s*[^/\n]+/\s*(\d+)\s*PACKAGES"
            r"[^/\n]*?(\d+\.?\d*)\s*KGS\s*/?\s*(\d+\.?\d*)\s*M",
            body,
            re.IGNORECASE,
        )
        if summary:
            _set(data, "number_of_packages", summary.group(2), source=source)
            _set(data, "gross_weight_kgs", summary.group(3), source=source)
            _set(data, "measurement_cbm", summary.group(4), source=source)

        packages_total = re.search(
            r"(\d+)\s+PACKAGES\s+IN\s+TOTAL",
            body,
            re.IGNORECASE,
        )
        if packages_total and data.number_of_packages.source == FieldSource.NOT_FOUND:
            _set(data, "number_of_packages", packages_total.group(1), source=source)

        weight_line = re.search(
            r"(\d+\.?\d*)\s*KGS\s+(\d+\.?\d*)\s*CBM",
            body,
            re.IGNORECASE,
        )
        if weight_line:
            if data.gross_weight_kgs.source == FieldSource.NOT_FOUND:
                _set(data, "gross_weight_kgs", weight_line.group(1), source=source)
            if data.measurement_cbm.source == FieldSource.NOT_FOUND:
                _set(data, "measurement_cbm", weight_line.group(2), source=source)

        desc = re.search(
            r"(\d+)\s+PACKAGES\s+IN\s+TOTAL\s*\n\s*(\d+X\d+[^\n]+SAID TO CONTAIN:)",
            body,
            re.IGNORECASE | re.DOTALL,
        )
        if desc:
            _set(
                data,
                "description_of_goods",
                f"{desc.group(1)} PACKAGES — {desc.group(2)[:200]}",
                source=source,
            )
        elif packages_total:
            _set(
                data,
                "description_of_goods",
                f"{packages_total.group(1)} PACKAGES IN TOTAL",
                source=source,
            )

        originals = re.search(
            r"\[(\d+)\]\s+ORIGINAL\s+BILLS?",
            body,
            re.IGNORECASE,
        )
        if originals:
            _set(data, "number_of_originals", originals.group(1), source=source)

        laden = re.search(
            r"DATE\s+LADEN\s+ON\s+BOARD\s*\n\s*([^\n]+)",
            body,
            re.IGNORECASE,
        )
        if laden:
            _set(data, "shipped_on_board_date", laden.group(1), source=source)

        _set(data, "carrier_name", "OCEAN NETWORK EXPRESS (ONE)", source=source)
        data.freight_terms = data.freight_terms or FreightTerms.from_text(body)
        data.containers = [Container(**c) for c in extract_containers(body)]

        return data

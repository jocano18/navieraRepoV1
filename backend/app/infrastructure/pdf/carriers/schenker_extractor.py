"""Schenker B/L layout — reduces false positives from header/legal blocks."""

import re

from app.domain.value_objects.extracted_field import ExtractedField
from app.domain.value_objects.field_source import FieldSource
from app.infrastructure.pdf.field_validation import is_plausible_field
from app.infrastructure.pdf.generic_bl_extractor import GenericBlExtractor
from app.infrastructure.pdf.text_preprocess import trim_boilerplate


class SchenkerExtractor(GenericBlExtractor):
    """Strategy for Schenker-forwarded bills of lading."""

    @property
    def carrier_key(self) -> str:
        return "SCHENKER"

    def extract_fields(self, text: str, *, source: FieldSource):
        """Parse Schenker-style B/L (booking / exporter blocks)."""
        body = trim_boilerplate(text)
        data = super().extract_fields(body, source=source)

        bl_patterns = [
            r"BILL\s+OF\s+LADING\s+NO\.?\s*[:\s]*([A-Z0-9][A-Z0-9\-/]{5,})",
            r"BOOKING\s+NO\.?\s*[:\s]*([A-Z0-9][A-Z0-9\-/]{5,})",
            r"DOCUMENT\s+NO\.?\s*[:\s]*([A-Z0-9][A-Z0-9\-/]{5,})",
            r"\b(SSZ\d{6,12})\b",
            r"\b(SCH[A-Z0-9]{6,14})\b",
        ]
        for pattern in bl_patterns:
            match = re.search(pattern, body, re.IGNORECASE)
            if match and is_plausible_field("bl_number", match.group(1)):
                data.bl_number = ExtractedField.from_value(
                    match.group(1).strip(),
                    source=source,
                )
                break

        shipper_match = re.search(
            r"(?:SHIPPER|EXPORTER)\s*(?:\([^)]*\))?\s*\n\s*([^\n/][^\n]{3,120})",
            body,
            re.IGNORECASE,
        )
        if shipper_match and is_plausible_field("shipper", shipper_match.group(1)):
            data.shipper = ExtractedField.from_value(
                shipper_match.group(1).strip(),
                source=source,
            )

        consignee_match = re.search(
            r"CONSIGNEE\s*(?:\([^)]*\))?\s*\n\s*([^\n/][^\n]{3,120})",
            body,
            re.IGNORECASE,
        )
        if consignee_match and is_plausible_field("consignee", consignee_match.group(1)):
            data.consignee = ExtractedField.from_value(
                consignee_match.group(1).strip(),
                source=source,
            )

        notify_match = re.search(
            r"NOTIFY\s+PARTY\s*(?:\([^)]*\))?\s*\n\s*([^\n(][^\n]{3,120})",
            body,
            re.IGNORECASE,
        )
        if notify_match and is_plausible_field("notify_party", notify_match.group(1)):
            data.notify_party = ExtractedField.from_value(
                notify_match.group(1).strip(),
                source=source,
            )

        vessel_match = re.search(
            r"(?:VESSEL|OCEAN\s+VESSEL)\s*(?:/|\s)+VOYAGE\s*[:\s]*\n?\s*([^\n]{4,80})",
            body,
            re.IGNORECASE,
        )
        if vessel_match and is_plausible_field("vessel_and_voyage", vessel_match.group(1)):
            data.vessel_and_voyage = ExtractedField.from_value(
                vessel_match.group(1).strip(),
                source=source,
            )

        data.carrier_name = ExtractedField.from_value("SCHENKER", source=source)
        data.containers = [
            c
            for c in data.containers
            if len(c.container_number) >= 10
        ]
        return data

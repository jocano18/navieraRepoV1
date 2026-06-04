"""AmassExtractor — carrier-specific Strategy for AMASS grid-form B/Ls."""

import re

from app.domain.entities.document_data import DocumentData
from app.domain.value_objects.extracted_field import ExtractedField
from app.domain.value_objects.field_source import FieldSource
from app.infrastructure.pdf.generic_bl_extractor import GenericBlExtractor


class AmassExtractor(GenericBlExtractor):
    """Strategy for AMASS LCL-LCL grid layout documents.

    Extends GenericBlExtractor and overrides fields that AMASS formats
    differently (proof of Open/Closed — register in Factory only).
    """

    @property
    def carrier_key(self) -> str:
        return "AMASS"

    def extract_fields(self, text: str, *, source: FieldSource) -> DocumentData:
        """Parse AMASS-specific layout then merge with generic fallbacks."""
        data = super().extract_fields(text, source=source)
        data.carrier_name = ExtractedField.from_value("AMASS", source=source)

        amass_bl = re.search(
            r"AMASS\s+(?:B/?L|BILL)\s*(?:NO)?\.?\s*[:\s]*([A-Z0-9\-/]+)",
            text,
            re.IGNORECASE,
        )
        if amass_bl:
            data.bl_number = ExtractedField.from_value(amass_bl.group(1), source=source)

        lcl_match = re.search(
            r"LCL[\s\-/]*LCL",
            text,
            re.IGNORECASE,
        )
        if lcl_match and data.description_of_goods.source == FieldSource.NOT_FOUND:
            data.description_of_goods = ExtractedField.from_value(
                "LCL/LCL CONSOLIDATED CARGO",
                source=source,
            )

        return data

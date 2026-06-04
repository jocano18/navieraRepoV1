"""GenericBlExtractor — keyword/regex parser for common B/L layouts (Strategy)."""

from app.application.ports.pdf_extraction_strategy import PdfExtractionStrategy
from app.domain.entities.container import Container
from app.domain.entities.document_data import DocumentData
from app.domain.value_objects.extracted_field import ExtractedField
from app.domain.value_objects.field_source import FieldSource
from app.domain.value_objects.freight_terms import FreightTerms
from app.infrastructure.pdf.field_patterns import extract_containers, search_field
from app.infrastructure.pdf.text_preprocess import trim_boilerplate


class GenericBlExtractor(PdfExtractionStrategy):
    """Strategy: label/keyword + regex extraction for most carrier layouts.

    Works for native and OCR text. Carrier-specific extractors can override
    individual fields without changing use cases (Open/Closed principle).
    """

    @property
    def carrier_key(self) -> str:
        return "GENERIC"

    def extract_fields(self, text: str, *, source: FieldSource) -> DocumentData:
        """Parse canonical fields from full document text."""
        text = trim_boilerplate(text)
        data = DocumentData(text_source=source)

        for field_name in data.scalar_fields():
            raw = search_field(text, field_name)
            setattr(
                data,
                field_name,
                ExtractedField.from_value(raw or "", source=source),
            )

        data.freight_terms = FreightTerms.from_text(text)
        data.containers = [Container(**c) for c in extract_containers(text)]

        # Fallback: first line matching B/L-like token if bl_number missing
        if data.bl_number.source == FieldSource.NOT_FOUND:
            import re

            fallback = re.search(
                r"\b([A-Z]{3,5}\d{6,12}[A-Z0-9]*)\b",
                text,
            )
            if fallback:
                data.bl_number = ExtractedField.from_value(
                    fallback.group(1),
                    source=source,
                )

        carrier_hint = search_field(text, "carrier_name")
        if not carrier_hint:
            for name in (
                "CMA CGM",
                "EVERGREEN",
                "AMASS",
                "ECU",
                "YQN",
                "SCHENKER",
                "ONE",
                "ONEY",
                "HAPAG",
                "MAERSK",
                "MSC",
                "ITPDA",
            ):
                if name in text.upper():
                    carrier_hint = name
                    break
        data.carrier_name = ExtractedField.from_value(
            carrier_hint or "",
            source=source,
        )

        return data

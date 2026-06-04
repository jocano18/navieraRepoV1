"""Extracted field with confidence/source metadata."""

from dataclasses import dataclass

from app.domain.value_objects.field_source import FieldSource


@dataclass(frozen=True)
class ExtractedField:
    """A single extracted document field with provenance.

    Attributes:
        value: Extracted text value (empty when NOT_FOUND).
        source: How the value was obtained (NATIVE, OCR, NOT_FOUND).
    """

    value: str
    source: FieldSource

    @classmethod
    def not_found(cls) -> "ExtractedField":
        """Create a NOT_FOUND placeholder field."""
        return cls(value="", source=FieldSource.NOT_FOUND)

    @classmethod
    def from_value(cls, value: str, *, source: FieldSource) -> "ExtractedField":
        """Create a field from a raw value and source."""
        cleaned = value.strip()
        if not cleaned:
            return cls.not_found()
        return cls(value=cleaned, source=source)

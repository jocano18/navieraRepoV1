"""Validation result — field-by-field comparison output."""

from dataclasses import dataclass, field

from app.domain.value_objects.field_source import FieldSource


@dataclass(frozen=True)
class FieldComparison:
    """Single field comparison between extracted and typed data.

    Attributes:
        field: Canonical field name.
        extracted_value: Value from PDF extraction.
        typed_value: Value entered by operator.
        matches: Whether values match (normalized).
        source: Extraction source for the PDF value.
    """

    field: str
    extracted_value: str
    typed_value: str
    matches: bool
    source: FieldSource


@dataclass
class ValidationResult:
    """Aggregate comparison result for a shipment.

    Attributes:
        shipment_id: Associated shipment UUID string.
        is_complete: True when all fields match.
        fields: Per-field comparison rows.
    """

    shipment_id: str
    is_complete: bool = False
    fields: list[FieldComparison] = field(default_factory=list)

    @property
    def mismatch_count(self) -> int:
        """Count fields that do not match."""
        return sum(1 for f in self.fields if not f.matches)

"""Domain service for comparing extracted vs digitized data."""

import re

from app.domain.entities.container import Container
from app.domain.entities.digitized_data import DigitizedData
from app.domain.entities.document_data import DocumentData
from app.domain.entities.validation_result import FieldComparison, ValidationResult


def _normalize(value: str) -> str:
    """Normalize a string for loose comparison."""
    collapsed = re.sub(r"\s+", " ", value.strip().upper())
    if collapsed in ("", "N/A", "NA", "-", "NONE", "NULL"):
        return ""
    return collapsed


class ComparisonService:
    """Produces field-by-field ValidationResult (domain logic, no I/O)."""

    @staticmethod
    def compare(
        shipment_id: str,
        extracted: DocumentData,
        digitized: DigitizedData,
    ) -> ValidationResult:
        """Compare extracted PDF data against operator-typed data.

        Args:
            shipment_id: Shipment identifier string.
            extracted: Data from PDF extraction.
            digitized: Data typed by operator.

        Returns:
            ValidationResult with per-field rows and is_complete flag.
        """
        comparisons: list[FieldComparison] = []

        for field_name, extracted_field in extracted.scalar_fields().items():
            typed_value = digitized.scalar_fields().get(field_name, "")
            matches = _normalize(extracted_field.value) == _normalize(typed_value)
            comparisons.append(
                FieldComparison(
                    field=field_name,
                    extracted_value=extracted_field.value,
                    typed_value=typed_value,
                    matches=matches,
                    source=extracted_field.source,
                )
            )

        freight_extracted = (
            extracted.freight_terms.value if extracted.freight_terms else ""
        )
        freight_typed = digitized.freight_terms.value if digitized.freight_terms else ""
        comparisons.append(
            FieldComparison(
                field="freight_terms",
                extracted_value=freight_extracted,
                typed_value=freight_typed,
                matches=_normalize(freight_extracted) == _normalize(freight_typed),
                source=extracted.text_source,
            )
        )

        container_match = ComparisonService._compare_containers(
            extracted.containers,
            digitized.containers,
        )
        comparisons.append(
            FieldComparison(
                field="containers",
                extracted_value=str(len(extracted.containers)),
                typed_value=str(len(digitized.containers)),
                matches=container_match,
                source=extracted.text_source,
            )
        )

        is_complete = all(c.matches for c in comparisons)
        return ValidationResult(
            shipment_id=shipment_id,
            is_complete=is_complete,
            fields=comparisons,
        )

    @staticmethod
    def _compare_containers(
        extracted: list[Container],
        digitized: list[Container],
    ) -> bool:
        """Compare container lists by container number sets."""
        ext_nums = {
            _normalize(c.container_number) for c in extracted if c.container_number
        }
        dig_nums = {
            _normalize(c.container_number) for c in digitized if c.container_number
        }
        if not ext_nums and not dig_nums:
            return True
        return ext_nums == dig_nums

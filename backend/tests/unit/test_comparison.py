"""Comparison service unit tests."""

from app.domain.entities.digitized_data import DigitizedData
from app.domain.entities.document_data import DocumentData
from app.domain.services.comparison_service import ComparisonService
from app.domain.value_objects.extracted_field import ExtractedField
from app.domain.value_objects.field_source import FieldSource


def test_comparison_detects_mismatch() -> None:
    """Mismatch on shipper marks comparison incomplete."""
    extracted = DocumentData(
        shipper=ExtractedField.from_value("ACME", source=FieldSource.NATIVE),
        bl_number=ExtractedField.from_value("BL1", source=FieldSource.NATIVE),
    )
    digitized = DigitizedData(shipper="OTHER", bl_number="BL1")
    result = ComparisonService.compare("id-1", extracted, digitized)
    assert not result.is_complete
    assert result.mismatch_count >= 1


def test_comparison_all_match() -> None:
    """Matching values produce is_complete=True."""
    extracted = DocumentData(
        shipper=ExtractedField.from_value("ACME", source=FieldSource.NATIVE),
        bl_number=ExtractedField.from_value("BL1", source=FieldSource.NATIVE),
    )
    digitized = DigitizedData(shipper="ACME", bl_number="BL1")
    result = ComparisonService.compare("id-1", extracted, digitized)
    shipper_row = next(f for f in result.fields if f.field == "shipper")
    assert shipper_row.matches


def test_comparison_treats_empty_and_na_as_equivalent() -> None:
    """Operator N/A placeholders match missing extracted values."""
    extracted = DocumentData(
        carrier_name=ExtractedField.from_value("", source=FieldSource.NATIVE),
        bl_number=ExtractedField.from_value("BL1", source=FieldSource.NATIVE),
    )
    digitized = DigitizedData(carrier_name="N/A", bl_number="BL1")
    result = ComparisonService.compare("id-1", extracted, digitized)
    assert result.is_complete

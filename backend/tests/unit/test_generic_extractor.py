"""GenericBlExtractor and CarrierDetector tests."""

from pathlib import Path

from app.domain.value_objects.field_source import FieldSource
from app.infrastructure.pdf.carrier_detector import CarrierDetector
from app.infrastructure.pdf.carriers.amass_extractor import AmassExtractor
from app.infrastructure.pdf.generic_bl_extractor import GenericBlExtractor


def test_generic_extractor_parses_bl_number() -> None:
    """Generic extractor finds B/L number from sample text."""
    text = (
        Path(__file__)
        .parent.parent.joinpath("fixtures/sample_bl.txt")
        .read_text(encoding="utf-8")
    )
    data = GenericBlExtractor().extract_fields(text, source=FieldSource.NATIVE)
    assert data.bl_number.value != ""
    assert data.bl_number.source == FieldSource.NATIVE
    assert "shipper" in data.shipper.value.lower() or data.shipper.value


def test_generic_extractor_finds_ports_and_weight() -> None:
    """Ports and weight fields are extracted from sample."""
    text = (
        Path(__file__)
        .parent.parent.joinpath("fixtures/sample_bl.txt")
        .read_text(encoding="utf-8")
    )
    data = GenericBlExtractor().extract_fields(text, source=FieldSource.NATIVE)
    assert data.port_of_loading.value
    assert data.port_of_discharge.value
    assert data.gross_weight_kgs.value


def test_amass_detector_and_extractor() -> None:
    """AMASS keyword routes to AmassExtractor via detector."""
    text = "AMASS BILL OF LADING NO: AMASS999\nSHIPPER: X\nCONSIGNEE: Y"
    key = CarrierDetector().detect(text)
    assert key == "AMASS"
    data = AmassExtractor().extract_fields(text, source=FieldSource.NATIVE)
    assert "AMASS" in data.carrier_name.value.upper()


def test_container_extraction() -> None:
    """Container numbers are parsed from text lines."""
    text = "Container MSCU1234567 40HC seal 123"
    data = GenericBlExtractor().extract_fields(text, source=FieldSource.NATIVE)
    assert len(data.containers) >= 1

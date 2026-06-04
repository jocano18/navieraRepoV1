"""ONE line B/L extractor tests."""

from pathlib import Path

from app.domain.value_objects.field_source import FieldSource
from app.infrastructure.pdf.carrier_detector import CarrierDetector
from app.infrastructure.pdf.carriers.one_extractor import OneExtractor


def test_carrier_detector_prefers_one_over_schenker() -> None:
    text = "SCHENKER INTERNATIONAL\nONEYTMEXE31234500\n(ONE), AS CARRIER"
    assert CarrierDetector().detect(text) == "ONE"


def test_one_extractor_parses_directo_bl() -> None:
    text = (
        Path(__file__)
        .parent.parent.joinpath("fixtures/sample_one_bl.txt")
        .read_text(encoding="utf-8")
    )
    data = OneExtractor().extract_fields(text, source=FieldSource.NATIVE)
    assert "ONEY" in data.bl_number.value
    assert "JOHNSON" in data.shipper.value.upper()
    assert "SUNRISE" in data.consignee.value.upper()
    assert data.port_of_loading.value == "MANZANILLO"
    assert "BUENAVENTURA" in data.port_of_discharge.value.upper()
    assert "COCHRANE" in data.vessel_and_voyage.value.upper()
    assert data.number_of_packages.value == "3932"
    assert "19619" in data.gross_weight_kgs.value
    assert len(data.containers) >= 1
    assert data.containers[0].container_number == "TCNU4440404"

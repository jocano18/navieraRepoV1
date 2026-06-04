"""PdfExtractionService — orchestrates native/OCR + Factory + Strategy."""

from pathlib import Path

from app.application.ports.ocr_engine import OcrEngine
from app.application.ports.pdf_extractor import PdfExtractor
from app.application.ports.pdf_text_extractor import PdfTextExtractor
from app.domain.entities.document_data import DocumentData
from app.domain.exceptions import PdfExtractionError
from app.domain.value_objects.bl_number import BlNumber
from app.domain.value_objects.field_source import FieldSource
from app.infrastructure.pdf.carrier_detector import CarrierDetector
from app.infrastructure.pdf.extractor_factory import ExtractorFactory


class PdfExtractionService(PdfExtractor):
    """Adapter implementing full two-step extraction pipeline.

    A) Text layer detection -> pdfplumber OR OCR fallback (Tesseract)
    B) CarrierDetector + ExtractorFactory + Strategy field parsing
    """

    def __init__(
        self,
        text_extractor: PdfTextExtractor,
        ocr_engine: OcrEngine,
        carrier_detector: CarrierDetector | None = None,
        factory: ExtractorFactory | None = None,
    ) -> None:
        self._text_extractor = text_extractor
        self._ocr_engine = ocr_engine
        self._carrier_detector = carrier_detector or CarrierDetector()
        self._factory = factory or ExtractorFactory()

    def extract(self, pdf_path: Path) -> DocumentData:
        """Run extraction pipeline on a PDF file."""
        if self._text_extractor.has_text_layer(pdf_path):
            text = self._text_extractor.extract_text(pdf_path)
            source = FieldSource.NATIVE
        else:
            text = self._ocr_engine.extract_text(pdf_path)
            source = FieldSource.OCR

        if not text.strip():
            raise PdfExtractionError("No text could be extracted from PDF")

        carrier_key = self._carrier_detector.detect(text)
        strategy = self._factory.get(carrier_key)
        document_data = strategy.extract_fields(text, source=source)
        document_data.text_source = source

        if not document_data.has_mandatory_fields():
            raise PdfExtractionError("Mandatory field bl_number could not be extracted")

        try:
            BlNumber(document_data.bl_number.value)
        except Exception as exc:
            raise PdfExtractionError(f"Invalid B/L number: {exc}") from exc

        return document_data

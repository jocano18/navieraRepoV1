"""PDF extraction pipeline port (native + OCR + Strategy + Factory)."""

from abc import ABC, abstractmethod
from pathlib import Path

from app.domain.entities.document_data import DocumentData


class PdfExtractor(ABC):
    """Port: full two-step extraction pipeline for a B/L PDF file."""

    @abstractmethod
    def extract(self, pdf_path: Path) -> DocumentData:
        """Extract canonical DocumentData from a PDF.

        Automatically selects native text or OCR fallback, detects carrier,
        and applies the appropriate Strategy via Factory.

        Raises:
            PdfExtractionError: On failure or missing mandatory fields.
        """

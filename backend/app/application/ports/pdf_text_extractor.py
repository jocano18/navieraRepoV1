"""PDF native text extraction port."""

from abc import ABC, abstractmethod
from pathlib import Path


class PdfTextExtractor(ABC):
    """Port for extracting text from PDFs with a usable text layer."""

    @abstractmethod
    def has_text_layer(self, pdf_path: Path) -> bool:
        """Detect whether the PDF has enough selectable text."""

    @abstractmethod
    def extract_text(self, pdf_path: Path) -> str:
        """Extract full document text via pdfplumber."""

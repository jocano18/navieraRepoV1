"""OCR engine port (Adapter pattern — Tesseract behind interface)."""

from abc import ABC, abstractmethod
from pathlib import Path


class OcrEngine(ABC):
    """Port for optical character recognition on scanned PDF pages."""

    @abstractmethod
    def extract_text(self, pdf_path: Path) -> str:
        """Render PDF pages and OCR them into plain text.

        Args:
            pdf_path: Path to the PDF file.

        Returns:
            Concatenated OCR text from all pages.
        """

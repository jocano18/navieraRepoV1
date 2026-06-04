"""PdfPlumberTextExtractor — native text layer extraction adapter."""

from pathlib import Path

import pdfplumber

from app.application.ports.pdf_text_extractor import PdfTextExtractor


class PdfPlumberTextExtractor(PdfTextExtractor):
    """Adapter: pdfplumber for native PDF text extraction."""

    MIN_CHARS_PER_PAGE = 50

    def has_text_layer(self, pdf_path: Path) -> bool:
        """Delegate to PyMuPDF detector if injected; else sample pdfplumber."""
        try:
            import fitz  # PyMuPDF

            doc = fitz.open(pdf_path)
            total = 0
            for page in doc:
                total += len(page.get_text().strip())
                if total >= self.MIN_CHARS_PER_PAGE:
                    doc.close()
                    return True
            doc.close()
            return False
        except ImportError:
            return len(self.extract_text(pdf_path).strip()) >= self.MIN_CHARS_PER_PAGE

    def extract_text(self, pdf_path: Path) -> str:
        """Extract text from all pages; prefer PyMuPDF for multi-page B/L forms."""
        try:
            import fitz

            doc = fitz.open(pdf_path)
            parts: list[str] = []
            for page in doc:
                text = page.get_text("text") or ""
                if len(text.strip()) < 30:
                    continue
                if "TERMS AND CONDITIONS" in text.upper()[:200]:
                    continue
                parts.append(text)
            doc.close()
            combined = "\n\n".join(parts)
            if len(combined.strip()) >= self.MIN_CHARS_PER_PAGE:
                return combined
        except ImportError:
            pass

        parts = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text() or ""
                if len(text.strip()) < 30:
                    continue
                if "TERMS AND CONDITIONS" in text.upper()[:200]:
                    continue
                parts.append(text)
        return "\n\n".join(parts)

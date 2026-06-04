"""TesseractOcrEngine — OCR fallback adapter (OcrEngine port)."""

from pathlib import Path

from app.application.ports.ocr_engine import OcrEngine


class TesseractOcrEngine(OcrEngine):
    """Adapter: pdf2image renders pages, pytesseract performs OCR.

    Used automatically when PyMuPDF detects no usable text layer
    (e.g. Evergreen scanned B/Ls with ORIGINAL watermark).
    """

    def extract_text(self, pdf_path: Path) -> str:
        """OCR all pages and return concatenated text."""
        try:
            import pytesseract
            from pdf2image import convert_from_path
        except ImportError as exc:
            msg = "OCR dependencies not installed: pdf2image, pytesseract"
            raise RuntimeError(msg) from exc

        images = convert_from_path(str(pdf_path), dpi=200)
        parts: list[str] = []
        for image in images:
            try:
                text = pytesseract.image_to_string(image, lang="eng+spa")
            except pytesseract.TesseractError:
                text = pytesseract.image_to_string(image, lang="eng")
            if text.strip():
                parts.append(text)
        return "\n\n".join(parts)

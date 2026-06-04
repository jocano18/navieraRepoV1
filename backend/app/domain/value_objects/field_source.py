"""Field extraction source value object."""

from enum import Enum


class FieldSource(str, Enum):
    """Indicates how a field value was obtained during PDF extraction.

    Attributes:
        NATIVE: Extracted from a selectable PDF text layer (pdfplumber).
        OCR: Extracted via Tesseract OCR fallback for scanned PDFs.
        NOT_FOUND: Field could not be located in the document.
        MANUAL: Entered by an operator (digitized data only).
    """

    NATIVE = "NATIVE"
    OCR = "OCR"
    NOT_FOUND = "NOT_FOUND"
    MANUAL = "MANUAL"

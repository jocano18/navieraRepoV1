"""PDF field parsing strategy port (Strategy pattern)."""

from abc import ABC, abstractmethod

from app.domain.entities.document_data import DocumentData
from app.domain.value_objects.field_source import FieldSource


class PdfExtractionStrategy(ABC):
    """Strategy: parse canonical B/L fields from plain text."""

    @property
    @abstractmethod
    def carrier_key(self) -> str:
        """Identifier for this strategy (e.g. GENERIC, AMASS)."""

    @abstractmethod
    def extract_fields(self, text: str, *, source: FieldSource) -> DocumentData:
        """Parse structured DocumentData from raw text.

        Args:
            text: Full document text (native or OCR).
            source: NATIVE or OCR — propagated to each field.
        """

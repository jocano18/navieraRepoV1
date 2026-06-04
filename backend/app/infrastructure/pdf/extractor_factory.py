"""ExtractorFactory — selects PdfExtractionStrategy by carrier key (Factory pattern)."""

from app.application.ports.pdf_extraction_strategy import PdfExtractionStrategy
from app.infrastructure.pdf.carriers.amass_extractor import AmassExtractor
from app.infrastructure.pdf.carriers.one_extractor import OneExtractor
from app.infrastructure.pdf.carriers.schenker_extractor import SchenkerExtractor
from app.infrastructure.pdf.generic_bl_extractor import GenericBlExtractor


class ExtractorFactory:
    """Factory: maps carrier detection result to a concrete Strategy.

    Register new carrier extractors here without modifying use cases.
    """

    def __init__(self) -> None:
        self._strategies: dict[str, PdfExtractionStrategy] = {
            "GENERIC": GenericBlExtractor(),
            "AMASS": AmassExtractor(),
            "SCHENKER": SchenkerExtractor(),
            "ONE": OneExtractor(),
        }

    def get(self, carrier_key: str) -> PdfExtractionStrategy:
        """Return strategy for carrier; defaults to GENERIC."""
        return self._strategies.get(carrier_key, self._strategies["GENERIC"])

    def register(self, carrier_key: str, strategy: PdfExtractionStrategy) -> None:
        """Register a new carrier-specific strategy at runtime."""
        self._strategies[carrier_key] = strategy

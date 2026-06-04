"""Freight terms value object."""

from enum import Enum


class FreightTerms(str, Enum):
    """Bill of Lading freight payment terms."""

    COLLECT = "COLLECT"
    PREPAID = "PREPAID"

    @classmethod
    def from_text(cls, text: str) -> "FreightTerms | None":
        """Parse freight terms from raw document text."""
        upper = text.upper()
        if "PREPAID" in upper:
            return cls.PREPAID
        if "COLLECT" in upper:
            return cls.COLLECT
        return None

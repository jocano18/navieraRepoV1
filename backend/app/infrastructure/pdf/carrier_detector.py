"""CarrierDetector — selects extractor strategy from document text."""

import re


class CarrierDetector:
    """Detects carrier from B/L text (name keywords + B/L number format).

    Used by ExtractorFactory (Factory pattern) to pick the right Strategy.
    """

    # Order matters: ONE before SCHENKER (Schenker often appears as agent on ONE B/Ls).
    _CARRIER_KEYWORDS: list[tuple[str, str]] = [
        ("AMASS", "AMASS"),
        ("OCEAN NETWORK EXPRESS", "ONE"),
        ("(ONE), AS CARRIER", "ONE"),
        ("ONEY", "ONE"),
        ("ONE LINE", "ONE"),
        ("CMA CGM", "GENERIC"),
        ("CMA-CGM", "GENERIC"),
        ("EVERGREEN", "GENERIC"),
        ("HAPAG", "GENERIC"),
        ("MAERSK", "GENERIC"),
        ("MSC ", "GENERIC"),
        ("ECU WORLDWIDE", "GENERIC"),
        ("ECU", "GENERIC"),
        ("YQN", "GENERIC"),
        ("TRIMAN", "GENERIC"),
        ("DC LOGISTICS", "GENERIC"),
        ("SCHENKER", "SCHENKER"),
        ("ITPDA", "GENERIC"),
    ]

    def detect(self, text: str) -> str:
        """Return carrier key for ExtractorFactory (e.g. ONE, AMASS, GENERIC)."""
        upper = text.upper()

        if re.search(r"\bONEY[A-Z0-9]{8,}\b", upper):
            return "ONE"

        for keyword, carrier_key in self._CARRIER_KEYWORDS:
            if keyword in upper and carrier_key != "GENERIC":
                return carrier_key

        if re.search(r"\bAMASS\b", upper):
            return "AMASS"

        return "GENERIC"

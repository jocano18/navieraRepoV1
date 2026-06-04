"""Shared regex patterns for B/L field extraction."""

import re

from app.infrastructure.pdf.field_validation import is_plausible_field

# ISO 6346: 4 letras + 7 dígitos (ej. TCNU4440404)
CONTAINER_PATTERN = re.compile(
    r"\b([A-Z]{4})(\d{7})\b",
    re.IGNORECASE,
)
CONTAINER_PATTERN_LEGACY = re.compile(
    r"\b([A-Z]{4}\d{7})\b",
    re.IGNORECASE,
)

FIELD_LABELS: dict[str, list[str]] = {
    "bl_number": [
        r"BILL\s+OF\s+LADING\s+NO\.?\s*[:\s]*([A-Z0-9][A-Z0-9\-/]{5,})",
        r"BOOKING\s+NO\.?\s*[:\s]*([A-Z0-9][A-Z0-9\-/]{5,})",
        r"B/?L\s*(?:NO|NUMBER|#|N[°º])?\.?\s*[:\s]*([A-Z0-9][A-Z0-9\-/]{5,})",
        r"BILL\s+OF\s+LADING\s+(?:NO|NUMBER)\s*[:\s]*([A-Z0-9\-/]{5,})",
        r"DOCUMENT\s+NO\.?\s*[:\s]*([A-Z0-9\-/]+)",
        r"CONOCIMIENTO\s+DE\s+EMBARQUE\s*(?:N[°º]|NO\.?)?\s*[:\s]*([A-Z0-9\-/]+)",
        r"(ITPDA\d{6,12})",
        r"(ONEY[A-Z0-9]{10,20})",
        r"(MILCTG\d{5,12})",
        r"B/L\s+NO\.?\s*:\s*(ONEY[A-Z0-9]{8,20})",
    ],
    "shipper": [
        r"SHIPPER\s*[:\s]*(.+?)(?:\n|CONSIGNEE|NOTIFY)",
        r"EXPORTADOR\s*[:\s]*(.+?)(?:\n|CONSIGNATARIO|CONSIGNEE|NOTIFY)",
    ],
    "consignee": [
        r"CONSIGNEE\s*[:\s]*(.+?)(?:\n|NOTIFY|DELIVERY)",
        r"CONSIGNATARIO\s*[:\s]*(.+?)(?:\n|NOTIFY|NOTIFICAR|DELIVERY)",
    ],
    "notify_party": [
        r"NOTIFY\s+PARTY(?:\s*/\s*ADDRESS)?\s*[:\s]*(.+?)(?:\n|DELIVERY|PORT)",
        r"NOTIFICAR\s+A\s*[:\s]*(.+?)(?:\n|DELIVERY|PUERTO|PORT)",
    ],
    "delivery_agent": [
        r"DELIVERY\s+AGENT\s*[:\s]*(.+?)(?:\n|PORT|VESSEL)",
    ],
    "vessel_and_voyage": [
        r"(?:OCEAN\s+)?VESSEL(?:\s*/\s*VOYAGE)?\s*[:\s]*(.+?)(?:\n|PORT|PLACE)",
    ],
    "place_of_receipt": [
        r"PLACE\s+OF\s+RECEIPT\s*[:\s]*(.+?)(?:\n|PORT)",
    ],
    "port_of_loading": [
        r"PORT\s+OF\s+LOADING\s*[:\s]*(.+?)(?:\n|PORT\s+OF\s+DISCHARGE)",
        r"PUERTO\s+DE\s+EMBARQUE\s*[:\s]*(.+?)(?:\n|PUERTO\s+DE\s+DESCARGA|PORT)",
    ],
    "port_of_discharge": [
        r"PORT\s+OF\s+DISCHARGE\s*[:\s]*(.+?)(?:\n|PLACE\s+OF\s+DELIVERY)",
        r"PUERTO\s+DE\s+DESCARGA\s*[:\s]*(.+?)(?:\n|LUGAR\s+DE\s+ENTREGA|PLACE)",
    ],
    "place_of_delivery": [
        r"PLACE\s+OF\s+DELIVERY\s*[:\s]*(.+?)(?:\n|MARKS|DESCRIPTION)",
        r"LUGAR\s+DE\s+ENTREGA\s*[:\s]*(.+?)(?:\n|MARKS|DESCRIPCI)",
    ],
    "marks_and_numbers": [
        r"MARKS\s*(?:AND|&)\s*NUMBERS\s*[:\s]*(.+?)(?:\n|DESCRIPTION)",
    ],
    "description_of_goods": [
        r"DESCRIPTION\s+OF\s+(?:GOODS|PACKAGES)\s*[:\s]*(.+?)(?:\n\s*GROSS|NUMBER\s+OF)",
    ],
    "number_of_packages": [
        r"(?:NUMBER|NO\.?)\s+OF\s+PACKAGES\s*[:\s]*([^\n]+)",
    ],
    "gross_weight_kgs": [
        r"GROSS\s+WEIGHT\s*[:\s]*([0-9.,\s]+)\s*(?:KGS?|KG)?",
    ],
    "measurement_cbm": [
        r"MEASUREMENT\s*[:\s]*([0-9.,\s]+)\s*(?:CBM|M3)?",
    ],
    "number_of_originals": [
        r"(?:NUMBER|NO\.?)\s+OF\s+ORIGINAL\s+B/?L\s*[:\s]*([0-9]+)",
    ],
    "shipped_on_board_date": [
        r"(?:SHIPPED\s+ON\s+BOARD|LADEN\s+ON\s+BOARD)(?:\s+DATE)?\s*[:\s]*([^\n]+)",
    ],
}


def search_field(text: str, field_name: str) -> str | None:
    """Search text for a canonical field using label patterns."""
    patterns = FIELD_LABELS.get(field_name, [])
    flags = re.IGNORECASE | re.MULTILINE | re.DOTALL
    for pattern in patterns:
        match = re.search(pattern, text, flags)
        if match:
            value = match.group(1).strip()
            value = re.sub(r"\s+", " ", value)
            if len(value) > 500:
                value = value[:500]
            if is_plausible_field(field_name, value):
                return value
    return None


def extract_containers(text: str) -> list[dict[str, str]]:
    """Extract container lines from text (ISO 6346)."""
    containers: list[dict[str, str]] = []
    seen: set[str] = set()

    def add(number: str) -> None:
        number = number.upper().replace(" ", "")
        if len(number) != 11 or number in seen:
            return
        seen.add(number)
        containers.append(
            {
                "container_number": number,
                "seal": "",
                "container_type": "",
                "packages": "",
                "gross_weight_kgs": "",
                "measurement_cbm": "",
            }
        )

    for match in CONTAINER_PATTERN.finditer(text):
        add(f"{match.group(1)}{match.group(2)}")
    for match in CONTAINER_PATTERN_LEGACY.finditer(text):
        add(match.group(1))
    return containers

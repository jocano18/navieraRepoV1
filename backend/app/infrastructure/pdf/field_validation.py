"""Heuristics to reject legal boilerplate mistaken for B/L field values."""

import re

_BOILERPLATE_PHRASES = (
    "IT IS AGREED",
    "NO RESPONSIBILITY",
    "RESPONSIBILITY SHALL",
    "HEREUNDER CONSTITUTES",
    "MERCHANT",
    "TERMS AND CONDITIONS",
    "FORWARDING AGENT-REFERENCES",
    "BOOKING NO. BILL OF LADING",
    "/EXPORTER BOOKING",
    "VOYAGE NO. FLAG",
    "PLACE OF BILL(S) ISSUE",
    "AS APPLICABLE",
    "DELIVERY OF THE GOODS",
    "CARRIER OR ITS AGENTS",
)

_LABEL_ONLY = frozenset(
    {
        "or",
        "to the",
        "as applicable",
        "for",
        "e",
        "vo",
        "voyage no. flag",
        "port of loading",
        "port of discharge",
    }
)


def is_plausible_field(field_name: str, value: str) -> bool:
    """Return False when a regex hit is clearly not real field content."""
    v = re.sub(r"\s+", " ", value.strip())
    if not v or v.lower() in _LABEL_ONLY:
        return False

    upper = v.upper()
    if any(phrase in upper for phrase in _BOILERPLATE_PHRASES):
        return False

    if field_name == "bl_number":
        if len(v) < 5 or not re.search(r"\d", v):
            return False
        if re.fullmatch(r"[A-Z]", v, re.IGNORECASE):
            return False

    if field_name in ("shipper", "consignee", "notify_party", "delivery_agent"):
        if len(v) < 4:
            return False
        if v.startswith(("/", "(", "IT IS", "** TO BE")):
            return False
        if "BOOKING NO" in upper and "BILL OF LADING" in upper:
            return False

    if field_name in (
        "port_of_loading",
        "port_of_discharge",
        "place_of_delivery",
        "place_of_receipt",
    ):
        if len(v) < 4:
            return False

    if field_name == "vessel_and_voyage":
        if upper in ("VOYAGE NO. FLAG", "VESSEL", "VOYAGE"):
            return False

    if field_name in ("marks_and_numbers", "description_of_goods"):
        if len(v) < 3:
            return False

    return True

"""Container entity for multi-container B/L documents."""

from dataclasses import dataclass


@dataclass
class Container:
    """Shipping container line on a Bill of Lading.

    Attributes:
        container_number: ISO container number (e.g. MSCU1234567).
        seal: Seal number.
        container_type: Size/type code (e.g. 40HC).
        packages: Number of packages in this container.
        gross_weight_kgs: Gross weight in kilograms.
        measurement_cbm: Volume in cubic meters.
    """

    container_number: str = ""
    seal: str = ""
    container_type: str = ""
    packages: str = ""
    gross_weight_kgs: str = ""
    measurement_cbm: str = ""

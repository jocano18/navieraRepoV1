"""Master / House Bill of Lading entity."""

from dataclasses import dataclass, field
from uuid import UUID

from app.domain.entities.container import Container


@dataclass
class HBL:
    """House Bill of Lading under a master MBL (consolidated cargo)."""

    hbl_number: str
    consignee: str = ""
    containers: list[Container] = field(default_factory=list)


@dataclass
class MBL:
    """Master Bill of Lading linked to a shipment.

    Attributes:
        id: Unique identifier.
        mbl_number: Master B/L number.
        is_master: True for master B/L in consolidated shipments.
        hbls: House bills (consolidado only).
        containers: Containers listed on this MBL.
    """

    id: UUID | None = None
    mbl_number: str = ""
    is_master: bool = True
    hbls: list[HBL] = field(default_factory=list)
    containers: list[Container] = field(default_factory=list)

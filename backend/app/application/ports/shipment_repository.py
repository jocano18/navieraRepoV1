"""Shipment repository port (Repository pattern)."""

from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.shipment import Shipment
from app.domain.value_objects.shipment_status import ShipmentStatus


class ShipmentRepository(ABC):
    """Port for Shipment aggregate persistence."""

    @abstractmethod
    async def get_by_id(self, shipment_id: UUID) -> Shipment | None:
        """Retrieve shipment by ID."""

    @abstractmethod
    async def save(self, shipment: Shipment) -> Shipment:
        """Persist shipment aggregate."""

    @abstractmethod
    async def list_all(
        self,
        *,
        status: ShipmentStatus | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Shipment]:
        """List shipments with optional status filter and pagination."""

    @abstractmethod
    async def delete(self, shipment_id: UUID) -> bool:
        """Delete shipment (for tests)."""

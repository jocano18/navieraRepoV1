"""Client repository port."""

from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.client import Client


class ClientRepository(ABC):
    """Port for client persistence."""

    @abstractmethod
    async def get_by_id(self, client_id: UUID) -> Client | None:
        """Retrieve client by ID."""

    @abstractmethod
    async def list_all(self) -> list[Client]:
        """List all clients."""

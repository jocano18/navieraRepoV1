"""Shipment PDF file storage port."""

from abc import ABC, abstractmethod
from pathlib import Path
from uuid import UUID


class FileStorage(ABC):
    """Port for storing shipment PDF copies outside the inbox."""

    @abstractmethod
    async def save_pdf(self, shipment_id: UUID, filename: str, content: bytes) -> Path:
        """Store PDF copy for a shipment."""

    @abstractmethod
    async def get_pdf_path(self, shipment_id: UUID) -> Path | None:
        """Return stored PDF path for viewing."""

    @abstractmethod
    async def read_pdf_bytes(self, shipment_id: UUID) -> bytes | None:
        """Read stored PDF bytes."""

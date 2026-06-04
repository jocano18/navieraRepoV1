"""Shipment PDF file storage adapter."""

from pathlib import Path
from uuid import UUID

from app.application.ports.file_storage import FileStorage
from app.infrastructure.config.settings import get_settings


class ShipmentFileStorage(FileStorage):
    """Stores shipment PDF copies under storage/shipments/{id}/."""

    def __init__(self, base_path: str | None = None) -> None:
        settings = get_settings()
        self._base = Path(base_path or settings.storage_local_path) / "shipments"
        self._base.mkdir(parents=True, exist_ok=True)

    def _shipment_dir(self, shipment_id: UUID) -> Path:
        path = self._base / str(shipment_id)
        path.mkdir(parents=True, exist_ok=True)
        return path

    async def save_pdf(self, shipment_id: UUID, filename: str, content: bytes) -> Path:
        dest = self._shipment_dir(shipment_id) / filename
        dest.write_bytes(content)
        return dest

    async def get_pdf_path(self, shipment_id: UUID) -> Path | None:
        directory = self._shipment_dir(shipment_id)
        pdfs = list(directory.glob("*.pdf"))
        return pdfs[0] if pdfs else None

    async def read_pdf_bytes(self, shipment_id: UUID) -> bytes | None:
        path = await self.get_pdf_path(shipment_id)
        return path.read_bytes() if path else None

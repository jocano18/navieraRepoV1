"""GetPdfFile use case — stream original PDF for frontend viewer."""

from uuid import UUID

from app.application.ports.file_storage import FileStorage
from app.application.ports.shipment_repository import ShipmentRepository
from app.domain.exceptions import ShipmentNotFoundError


class GetPdfFileUseCase:
    """Return original PDF bytes for a shipment."""

    def __init__(
        self,
        shipment_repo: ShipmentRepository,
        file_storage: FileStorage,
    ) -> None:
        self._shipment_repo = shipment_repo
        self._file_storage = file_storage

    async def execute(self, shipment_id: UUID) -> tuple[bytes, str]:
        """Return (pdf_bytes, filename)."""
        shipment = await self._shipment_repo.get_by_id(shipment_id)
        if shipment is None:
            raise ShipmentNotFoundError(f"Shipment {shipment_id} not found")
        pdf_bytes = await self._file_storage.read_pdf_bytes(shipment_id)
        if pdf_bytes is None:
            raise ShipmentNotFoundError("PDF file not found")
        return pdf_bytes, shipment.source_pdf_filename

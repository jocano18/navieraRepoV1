"""ExtractPdfData use case."""

from uuid import UUID

from app.application.ports.file_storage import FileStorage
from app.application.ports.pdf_extractor import PdfExtractor
from app.application.ports.shipment_repository import ShipmentRepository
from app.domain.entities.document_data import DocumentData
from app.domain.exceptions import ShipmentNotFoundError, ValidationIncompleteError
from app.domain.value_objects.shipment_status import ShipmentStatus


class ExtractPdfDataUseCase:
    """Run PDF extraction pipeline and transition to EXTRAIDO."""

    def __init__(
        self,
        shipment_repo: ShipmentRepository,
        pdf_extractor: PdfExtractor,
        file_storage: FileStorage,
    ) -> None:
        self._shipment_repo = shipment_repo
        self._pdf_extractor = pdf_extractor
        self._file_storage = file_storage

    async def execute(self, shipment_id: UUID) -> DocumentData:
        """Extract data from shipment PDF."""
        shipment = await self._shipment_repo.get_by_id(shipment_id)
        if shipment is None:
            raise ShipmentNotFoundError(f"Shipment {shipment_id} not found")
        if shipment.status != ShipmentStatus.PENDIENTE_EXTRACCION:
            raise ValidationIncompleteError(
                f"Cannot extract in status {shipment.status.value}"
            )
        pdf_path = await self._file_storage.get_pdf_path(shipment_id)
        if pdf_path is None:
            raise ShipmentNotFoundError("Stored PDF not found for shipment")

        document_data = self._pdf_extractor.extract(pdf_path)
        shipment.record_extraction(document_data)
        await self._shipment_repo.save(shipment)
        return document_data

"""CreateShipment use case."""

from app.application.dto.shipment_dto import CreateShipmentInput, CreateShipmentOutput
from app.application.ports.client_repository import ClientRepository
from app.application.ports.file_storage import FileStorage
from app.application.ports.inbox_storage import InboxStorage
from app.application.ports.shipment_repository import ShipmentRepository
from app.domain.entities.shipment import Shipment
from app.domain.exceptions import ClientNotFoundError, InboxFileNotFoundError


class CreateShipmentUseCase:
    """Create a shipment from an inbox PDF filename."""

    def __init__(
        self,
        shipment_repo: ShipmentRepository,
        inbox: InboxStorage,
        file_storage: FileStorage,
        client_repo: ClientRepository | None = None,
    ) -> None:
        self._shipment_repo = shipment_repo
        self._inbox = inbox
        self._file_storage = file_storage
        self._client_repo = client_repo

    async def execute(self, input_dto: CreateShipmentInput) -> CreateShipmentOutput:
        """Create shipment and copy PDF to storage."""
        if self._client_repo is not None:
            client = await self._client_repo.get_by_id(input_dto.client_id)
            if client is None:
                raise ClientNotFoundError(
                    f"Client {input_dto.client_id} not found. "
                    "Run database seed or restart the backend container."
                )

        try:
            pdf_bytes = self._inbox.read_bytes(input_dto.source_pdf_filename)
        except InboxFileNotFoundError as exc:
            raise exc

        reference = input_dto.reference or input_dto.source_pdf_filename
        shipment = Shipment.create(
            reference=reference,
            source_pdf_filename=input_dto.source_pdf_filename,
            cargo_type=input_dto.cargo_type,
            client_id=input_dto.client_id,
        )
        await self._file_storage.save_pdf(
            shipment.id,
            input_dto.source_pdf_filename,
            pdf_bytes,
        )
        saved = await self._shipment_repo.save(shipment)
        return CreateShipmentOutput(
            shipment_id=saved.id,
            reference=saved.reference,
            status=saved.status,
        )

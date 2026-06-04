"""ApproveShipment use case — COMPLETO -> NOTIFICADO + notify client."""

from uuid import UUID

from app.application.ports.client_repository import ClientRepository
from app.application.ports.event_publisher import EventPublisher
from app.application.ports.file_storage import FileStorage
from app.application.ports.notifier import Notifier
from app.application.ports.shipment_repository import ShipmentRepository
from app.domain.exceptions import ClientNotFoundError, ShipmentNotFoundError
from app.domain.value_objects.shipment_status import ShipmentStatus
from app.infrastructure.notifications.approval_token import ApprovalTokenService
from app.infrastructure.notifications.email_templates import build_approval_email


class ApproveShipmentUseCase:
    """Executive approves shipment and notifies client (Observer via events)."""

    def __init__(
        self,
        shipment_repo: ShipmentRepository,
        client_repo: ClientRepository,
        notifier: Notifier,
        file_storage: FileStorage,
        event_publisher: EventPublisher,
        approval_tokens: ApprovalTokenService,
    ) -> None:
        self._shipment_repo = shipment_repo
        self._client_repo = client_repo
        self._notifier = notifier
        self._file_storage = file_storage
        self._event_publisher = event_publisher
        self._approval_tokens = approval_tokens

    async def execute(self, shipment_id: UUID) -> None:
        """Approve and send notification with PDF attached."""
        shipment = await self._shipment_repo.get_by_id(shipment_id)
        if shipment is None:
            raise ShipmentNotFoundError(f"Shipment {shipment_id} not found")
        if shipment.status != ShipmentStatus.COMPLETO:
            from app.domain.exceptions import ValidationIncompleteError

            raise ValidationIncompleteError(
                f"Cannot approve in status {shipment.status.value}"
            )

        client = await self._client_repo.get_by_id(shipment.client_id)
        if client is None:
            raise ClientNotFoundError(f"Client {shipment.client_id} not found")

        shipment.approve_and_notify()
        pdf_path = await self._file_storage.get_pdf_path(shipment_id)
        approval_url = self._approval_tokens.build_approval_url(shipment_id)
        plain, html = build_approval_email(
            client_name=client.name,
            reference=shipment.reference,
            approval_url=approval_url,
        )

        await self._notifier.notify(
            client.email,
            subject=f"Documentación lista — {shipment.reference}",
            body=plain,
            html_body=html,
            attachment_path=pdf_path,
            shipment_id=shipment_id,
        )

        for event in shipment.pull_events():
            await self._event_publisher.publish(event)

        await self._shipment_repo.save(shipment)

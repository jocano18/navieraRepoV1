"""ClientApprove use case — NOTIFICADO -> APROBADO_CLIENTE."""

from uuid import UUID

from app.application.ports.shipment_repository import ShipmentRepository
from app.domain.exceptions import ShipmentNotFoundError, ValidationIncompleteError
from app.domain.value_objects.shipment_status import ShipmentStatus


class ClientApproveUseCase:
    """Record client approval after notification."""

    def __init__(self, shipment_repo: ShipmentRepository) -> None:
        self._shipment_repo = shipment_repo

    async def execute(self, shipment_id: UUID) -> None:
        """Transition NOTIFICADO -> APROBADO_CLIENTE."""
        shipment = await self._shipment_repo.get_by_id(shipment_id)
        if shipment is None:
            raise ShipmentNotFoundError(f"Shipment {shipment_id} not found")
        if shipment.status != ShipmentStatus.NOTIFICADO:
            raise ValidationIncompleteError(
                f"Cannot client-approve in status {shipment.status.value}"
            )
        shipment.mark_client_approved()
        await self._shipment_repo.save(shipment)

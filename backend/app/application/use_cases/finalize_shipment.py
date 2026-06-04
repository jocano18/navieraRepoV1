"""Finalize shipment — APROBADO_CLIENTE -> FINALIZADO."""

from uuid import UUID

from app.application.ports.shipment_repository import ShipmentRepository
from app.domain.exceptions import ShipmentNotFoundError, ValidationIncompleteError
from app.domain.value_objects.shipment_status import ShipmentStatus


class FinalizeShipmentUseCase:
    """Mark shipment as FINALIZADO after client approval."""

    def __init__(self, shipment_repo: ShipmentRepository) -> None:
        self._shipment_repo = shipment_repo

    async def execute(self, shipment_id: UUID) -> None:
        """Transition to FINALIZADO."""
        shipment = await self._shipment_repo.get_by_id(shipment_id)
        if shipment is None:
            raise ShipmentNotFoundError(f"Shipment {shipment_id} not found")
        if shipment.status != ShipmentStatus.APROBADO_CLIENTE:
            raise ValidationIncompleteError(
                f"Cannot finalize in status {shipment.status.value}"
            )
        shipment.finalize()
        await self._shipment_repo.save(shipment)

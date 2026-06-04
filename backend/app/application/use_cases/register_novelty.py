"""RegisterNovelty use case."""

from uuid import UUID

from app.application.ports.shipment_repository import ShipmentRepository
from app.domain.exceptions import ShipmentNotFoundError
from app.domain.value_objects.shipment_status import ShipmentStatus


class RegisterNoveltyUseCase:
    """Register a novelty: APROBADO_CLIENTE -> CON_NOVEDAD."""

    def __init__(self, shipment_repo: ShipmentRepository) -> None:
        self._shipment_repo = shipment_repo

    async def execute(
        self,
        shipment_id: UUID,
        description: str,
    ) -> None:
        """Register novelty description and transition."""
        shipment = await self._shipment_repo.get_by_id(shipment_id)
        if shipment is None:
            raise ShipmentNotFoundError(f"Shipment {shipment_id} not found")
        if shipment.status != ShipmentStatus.APROBADO_CLIENTE:
            from app.domain.exceptions import ValidationIncompleteError

            raise ValidationIncompleteError(
                "Novelty can only be registered after client approval"
            )
        shipment.register_novelty(description)
        shipment.transition_to(ShipmentStatus.EN_VALIDACION)
        await self._shipment_repo.save(shipment)

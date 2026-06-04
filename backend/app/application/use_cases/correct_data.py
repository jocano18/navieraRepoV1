"""CorrectData use case."""

from uuid import UUID

from app.application.dto.shipment_dto import DigitizedDataInput
from app.application.ports.shipment_repository import ShipmentRepository
from app.application.use_cases._mappers import digitized_from_input
from app.domain.exceptions import ShipmentNotFoundError
from app.domain.value_objects.shipment_status import ShipmentStatus


class CorrectDataUseCase:
    """Patch digitized data after INCOMPLETO validation."""

    def __init__(self, shipment_repo: ShipmentRepository) -> None:
        self._shipment_repo = shipment_repo

    async def execute(
        self,
        shipment_id: UUID,
        input_dto: DigitizedDataInput,
    ) -> None:
        """Update digitized fields and return to EN_VALIDACION."""
        shipment = await self._shipment_repo.get_by_id(shipment_id)
        if shipment is None:
            raise ShipmentNotFoundError(f"Shipment {shipment_id} not found")
        shipment.digitized_data = digitized_from_input(input_dto)
        if shipment.status == ShipmentStatus.INCOMPLETO:
            shipment.transition_to(ShipmentStatus.EN_VALIDACION)
        await self._shipment_repo.save(shipment)

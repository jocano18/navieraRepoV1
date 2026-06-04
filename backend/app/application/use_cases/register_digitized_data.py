"""RegisterDigitizedData use case."""

from uuid import UUID

from app.application.dto.shipment_dto import DigitizedDataInput
from app.application.ports.shipment_repository import ShipmentRepository
from app.application.use_cases._mappers import digitized_from_input
from app.domain.exceptions import ShipmentNotFoundError


class RegisterDigitizedDataUseCase:
    """Register operator-typed data and transition to EN_DIGITACION."""

    def __init__(self, shipment_repo: ShipmentRepository) -> None:
        self._shipment_repo = shipment_repo

    async def execute(
        self,
        shipment_id: UUID,
        input_dto: DigitizedDataInput,
    ) -> None:
        """Persist digitized data."""
        shipment = await self._shipment_repo.get_by_id(shipment_id)
        if shipment is None:
            raise ShipmentNotFoundError(f"Shipment {shipment_id} not found")
        digitized = digitized_from_input(input_dto)
        shipment.record_digitized(digitized)
        shipment.submit_for_validation()
        await self._shipment_repo.save(shipment)

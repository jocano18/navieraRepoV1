"""GetShipment use case."""

from uuid import UUID

from app.application.dto.shipment_dto import ShipmentDetailOutput
from app.application.ports.shipment_repository import ShipmentRepository
from app.application.use_cases._mappers import shipment_to_detail
from app.domain.exceptions import ShipmentNotFoundError


class GetShipmentUseCase:
    """Retrieve a single shipment by ID."""

    def __init__(self, shipment_repo: ShipmentRepository) -> None:
        self._shipment_repo = shipment_repo

    async def execute(self, shipment_id: UUID) -> ShipmentDetailOutput:
        """Return shipment detail."""
        shipment = await self._shipment_repo.get_by_id(shipment_id)
        if shipment is None:
            raise ShipmentNotFoundError(f"Shipment {shipment_id} not found")
        return shipment_to_detail(shipment)

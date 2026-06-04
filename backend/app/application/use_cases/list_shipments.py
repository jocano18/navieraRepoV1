"""ListShipments use case."""

from app.application.dto.shipment_dto import ShipmentListItem
from app.application.ports.shipment_repository import ShipmentRepository
from app.application.use_cases._mappers import shipment_to_list_item
from app.domain.value_objects.shipment_status import ShipmentStatus


class ListShipmentsUseCase:
    """List shipments with optional status filter."""

    def __init__(self, shipment_repo: ShipmentRepository) -> None:
        self._shipment_repo = shipment_repo

    async def execute(
        self,
        *,
        status: ShipmentStatus | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[ShipmentListItem]:
        """Return shipment summaries."""
        shipments = await self._shipment_repo.list_all(
            status=status,
            skip=skip,
            limit=limit,
        )
        return [shipment_to_list_item(s) for s in shipments]

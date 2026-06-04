"""CompareData use case."""

from uuid import UUID

from app.application.dto.shipment_dto import ComparisonOutput
from app.application.ports.shipment_repository import ShipmentRepository
from app.domain.exceptions import ShipmentNotFoundError, ValidationIncompleteError
from app.domain.services.comparison_service import ComparisonService


class CompareDataUseCase:
    """Produce field-by-field comparison for executive review."""

    def __init__(self, shipment_repo: ShipmentRepository) -> None:
        self._shipment_repo = shipment_repo

    async def execute(self, shipment_id: UUID) -> ComparisonOutput:
        """Compare extracted vs digitized data."""
        shipment = await self._shipment_repo.get_by_id(shipment_id)
        if shipment is None:
            raise ShipmentNotFoundError(f"Shipment {shipment_id} not found")
        if not shipment.extracted_data or not shipment.digitized_data:
            raise ValidationIncompleteError(
                "Both extracted and digitized data are required"
            )
        result = ComparisonService.compare(
            str(shipment_id),
            shipment.extracted_data,
            shipment.digitized_data,
        )
        return ComparisonOutput(
            shipment_id=shipment_id,
            is_complete=result.is_complete,
            fields=result.fields,
        )

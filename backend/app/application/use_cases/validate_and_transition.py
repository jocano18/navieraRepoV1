"""ValidateAndTransition use case."""

from uuid import UUID

from app.application.dto.shipment_dto import (
    ValidateShipmentInput,
    ValidateShipmentOutput,
)
from app.application.ports.shipment_repository import ShipmentRepository
from app.domain.exceptions import ShipmentNotFoundError, ValidationIncompleteError
from app.domain.services.comparison_service import ComparisonService
from app.domain.value_objects.shipment_status import ShipmentStatus


class ValidateAndTransitionUseCase:
    """Executive validates: EN_VALIDACION -> INCOMPLETO | COMPLETO."""

    def __init__(self, shipment_repo: ShipmentRepository) -> None:
        self._shipment_repo = shipment_repo

    async def execute(
        self,
        shipment_id: UUID,
        input_dto: ValidateShipmentInput,
    ) -> ValidateShipmentOutput:
        """Run comparison and apply status transition."""
        shipment = await self._shipment_repo.get_by_id(shipment_id)
        if shipment is None:
            raise ShipmentNotFoundError(f"Shipment {shipment_id} not found")
        if shipment.status != ShipmentStatus.EN_VALIDACION:
            raise ValidationIncompleteError(
                f"Cannot validate in status {shipment.status.value}"
            )
        if not shipment.extracted_data or not shipment.digitized_data:
            raise ValidationIncompleteError("Missing extracted or digitized data")

        result = ComparisonService.compare(
            str(shipment_id),
            shipment.extracted_data,
            shipment.digitized_data,
        )
        if input_dto.mark_complete and not result.is_complete:
            raise ValidationIncompleteError(
                "Cannot mark complete: field mismatches remain"
            )
        from app.domain.entities.validation_result import ValidationResult

        forced_complete = input_dto.mark_complete and result.is_complete
        forced_result = ValidationResult(
            shipment_id=str(shipment_id),
            is_complete=forced_complete,
            fields=result.fields,
        )
        shipment.apply_validation(forced_result)

        await self._shipment_repo.save(shipment)
        return ValidateShipmentOutput(
            shipment_id=shipment_id,
            new_status=shipment.status,
        )

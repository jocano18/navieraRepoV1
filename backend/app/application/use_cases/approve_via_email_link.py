"""ApproveViaEmailLink — client clicks email button → approve + finalize."""

from dataclasses import dataclass
from uuid import UUID

from app.application.ports.shipment_repository import ShipmentRepository
from app.domain.exceptions import ShipmentNotFoundError, ValidationIncompleteError
from app.domain.value_objects.shipment_status import ShipmentStatus
from app.infrastructure.notifications.approval_token import ApprovalTokenService


@dataclass(frozen=True)
class ApproveViaEmailLinkResult:
    """Outcome of processing an email approval link."""

    shipment_id: UUID
    reference: str
    status: ShipmentStatus
    already_finalized: bool


class ApproveViaEmailLinkUseCase:
    """Validate token and complete client approval through FINALIZADO."""

    def __init__(
        self,
        shipment_repo: ShipmentRepository,
        token_service: ApprovalTokenService,
    ) -> None:
        self._shipment_repo = shipment_repo
        self._token_service = token_service

    async def execute(self, token: str) -> ApproveViaEmailLinkResult:
        """Process approval link: NOTIFICADO → APROBADO_CLIENTE → FINALIZADO."""
        shipment_id = self._token_service.verify(token)
        shipment = await self._shipment_repo.get_by_id(shipment_id)
        if shipment is None:
            raise ShipmentNotFoundError(f"Shipment {shipment_id} not found")

        if shipment.status == ShipmentStatus.FINALIZADO:
            return ApproveViaEmailLinkResult(
                shipment_id=shipment.id,
                reference=shipment.reference,
                status=shipment.status,
                already_finalized=True,
            )

        if shipment.status == ShipmentStatus.NOTIFICADO:
            shipment.mark_client_approved()
            await self._shipment_repo.save(shipment)

        if shipment.status == ShipmentStatus.APROBADO_CLIENTE:
            shipment.finalize()
            await self._shipment_repo.save(shipment)
            return ApproveViaEmailLinkResult(
                shipment_id=shipment.id,
                reference=shipment.reference,
                status=shipment.status,
                already_finalized=False,
            )

        raise ValidationIncompleteError(
            f"No se puede aprobar por correo en estado {shipment.status.value}. "
            "Solicite un nuevo enlace a su ejecutivo."
        )

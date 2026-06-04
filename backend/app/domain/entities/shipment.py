"""Shipment aggregate root."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4

from app.domain.entities.digitized_data import DigitizedData
from app.domain.entities.document_data import DocumentData
from app.domain.entities.mbl import MBL
from app.domain.entities.validation_result import ValidationResult
from app.domain.events.shipment_events import (
    DomainEvent,
    ShipmentApprovedEvent,
    ShipmentCompletedEvent,
    ShipmentNotifiedEvent,
    ShipmentRejectedEvent,
)
from app.domain.exceptions import InvalidStateTransitionError, ValidationIncompleteError
from app.domain.state_machine.state import ShipmentStateFactory
from app.domain.value_objects.cargo_type import CargoType
from app.domain.value_objects.shipment_status import ShipmentStatus


@dataclass
class Shipment:
    """Aggregate root for the shipment documentation workflow.

    Owns status transitions via the State pattern and collects domain events
    for the Observer pattern in the application layer.
    """

    id: UUID
    reference: str
    source_pdf_filename: str
    cargo_type: CargoType
    status: ShipmentStatus
    client_id: UUID
    mbls: list[MBL] = field(default_factory=list)
    extracted_data: DocumentData | None = None
    digitized_data: DigitizedData | None = None
    validation_result: ValidationResult | None = None
    novelty_description: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    _events: list[DomainEvent] = field(default_factory=list, repr=False)

    @classmethod
    def create(
        cls,
        *,
        reference: str,
        source_pdf_filename: str,
        cargo_type: CargoType,
        client_id: UUID,
    ) -> Shipment:
        """Factory for a new shipment in PENDIENTE_EXTRACCION."""
        return cls(
            id=uuid4(),
            reference=reference,
            source_pdf_filename=source_pdf_filename,
            cargo_type=cargo_type,
            status=ShipmentStatus.PENDIENTE_EXTRACCION,
            client_id=client_id,
        )

    def transition_to(self, target: ShipmentStatus) -> None:
        """Transition to a new status using the state machine."""
        new_status = ShipmentStateFactory.validate_transition(self.status, target)
        self.status = new_status
        self.updated_at = datetime.now(UTC)
        self._emit_events_for(target)

    def reject(self, reason: str = "") -> None:
        """Reject shipment from any non-terminal state."""
        if self.status in (ShipmentStatus.FINALIZADO, ShipmentStatus.RECHAZADO):
            msg = f"Cannot reject shipment in {self.status.value}"
            raise InvalidStateTransitionError(msg)
        self.status = ShipmentStatus.RECHAZADO
        self.updated_at = datetime.now(UTC)
        self._events.append(ShipmentRejectedEvent(shipment_id=self.id, reason=reason))

    def record_extraction(self, data: DocumentData) -> None:
        """Store extracted data and move to EXTRAIDO."""
        self.extracted_data = data
        self.transition_to(ShipmentStatus.EXTRAIDO)

    def record_digitized(self, data: DigitizedData) -> None:
        """Store digitized data; transition EXTRAIDO -> EN_DIGITACION if needed."""
        self.digitized_data = data
        if self.status == ShipmentStatus.EXTRAIDO:
            self.transition_to(ShipmentStatus.EN_DIGITACION)

    def submit_for_validation(self) -> None:
        """Move EN_DIGITACION -> EN_VALIDACION."""
        if not self.digitized_data:
            raise ValidationIncompleteError("Digitized data is required")
        self.transition_to(ShipmentStatus.EN_VALIDACION)

    def apply_validation(self, result: ValidationResult) -> None:
        """Apply validation outcome: INCOMPLETO or COMPLETO."""
        self.validation_result = result
        target = (
            ShipmentStatus.COMPLETO if result.is_complete else ShipmentStatus.INCOMPLETO
        )
        self.transition_to(target)

    def approve_and_notify(self) -> None:
        """Executive approval: COMPLETO -> NOTIFICADO."""
        self.transition_to(ShipmentStatus.NOTIFICADO)

    def mark_client_approved(self) -> None:
        """NOTIFICADO -> APROBADO_CLIENTE."""
        self.transition_to(ShipmentStatus.APROBADO_CLIENTE)

    def finalize(self) -> None:
        """APROBADO_CLIENTE -> FINALIZADO."""
        self.transition_to(ShipmentStatus.FINALIZADO)

    def register_novelty(self, description: str) -> None:
        """Register novelty: APROBADO_CLIENTE -> CON_NOVEDAD."""
        self.novelty_description = description
        self.transition_to(ShipmentStatus.CON_NOVEDAD)

    def pull_events(self) -> list[DomainEvent]:
        """Return and clear pending domain events (Observer dispatch)."""
        events = list(self._events)
        self._events.clear()
        return events

    def _emit_events_for(self, target: ShipmentStatus) -> None:
        """Emit domain events for significant transitions."""
        if target == ShipmentStatus.COMPLETO:
            self._events.append(ShipmentCompletedEvent(shipment_id=self.id))
        elif target == ShipmentStatus.NOTIFICADO:
            self._events.append(
                ShipmentNotifiedEvent(shipment_id=self.id, client_id=self.client_id)
            )
        elif target == ShipmentStatus.APROBADO_CLIENTE:
            self._events.append(ShipmentApprovedEvent(shipment_id=self.id))

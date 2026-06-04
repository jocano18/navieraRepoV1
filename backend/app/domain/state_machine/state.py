"""Shipment state machine — State pattern (no scattered if/else)."""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.exceptions import InvalidStateTransitionError
from app.domain.value_objects.shipment_status import ShipmentStatus

# Transition map: current -> allowed targets (State pattern via lookup table)
_ALLOWED: dict[ShipmentStatus, frozenset[ShipmentStatus]] = {
    ShipmentStatus.PENDIENTE_EXTRACCION: frozenset({ShipmentStatus.EXTRAIDO}),
    ShipmentStatus.EXTRAIDO: frozenset({ShipmentStatus.EN_DIGITACION}),
    ShipmentStatus.EN_DIGITACION: frozenset({ShipmentStatus.EN_VALIDACION}),
    ShipmentStatus.EN_VALIDACION: frozenset(
        {ShipmentStatus.INCOMPLETO, ShipmentStatus.COMPLETO}
    ),
    ShipmentStatus.INCOMPLETO: frozenset({ShipmentStatus.EN_VALIDACION}),
    ShipmentStatus.COMPLETO: frozenset({ShipmentStatus.NOTIFICADO}),
    ShipmentStatus.NOTIFICADO: frozenset({ShipmentStatus.APROBADO_CLIENTE}),
    ShipmentStatus.APROBADO_CLIENTE: frozenset(
        {ShipmentStatus.CON_NOVEDAD, ShipmentStatus.FINALIZADO}
    ),
    ShipmentStatus.CON_NOVEDAD: frozenset({ShipmentStatus.EN_VALIDACION}),
    ShipmentStatus.FINALIZADO: frozenset(),
    ShipmentStatus.RECHAZADO: frozenset(),
}

_TERMINAL = frozenset({ShipmentStatus.FINALIZADO, ShipmentStatus.RECHAZADO})


class ShipmentState(ABC):
    """Abstract state — each subclass encapsulates allowed transitions."""

    @property
    @abstractmethod
    def status(self) -> ShipmentStatus:
        """Return the enum value for this state."""

    def can_transition_to(self, target: ShipmentStatus) -> bool:
        """Check if transition to target is allowed."""
        allowed = _ALLOWED.get(self.status, frozenset())
        if target == ShipmentStatus.RECHAZADO and self.status not in _TERMINAL:
            return True
        return target in allowed

    def transition_to(self, target: ShipmentStatus) -> ShipmentState:
        """Validate and return the new state instance."""
        if not self.can_transition_to(target):
            msg = f"Cannot transition from {self.status.value} to {target.value}"
            raise InvalidStateTransitionError(msg)
        return ShipmentStateFactory.create(target)


class PendienteExtraccionState(ShipmentState):
    """Awaiting PDF extraction."""

    @property
    def status(self) -> ShipmentStatus:
        return ShipmentStatus.PENDIENTE_EXTRACCION


class ExtraidoState(ShipmentState):
    """PDF extracted."""

    @property
    def status(self) -> ShipmentStatus:
        return ShipmentStatus.EXTRAIDO


class EnDigitacionState(ShipmentState):
    """Operator entering digitized data."""

    @property
    def status(self) -> ShipmentStatus:
        return ShipmentStatus.EN_DIGITACION


class EnValidacionState(ShipmentState):
    """Executive comparing extracted vs typed data."""

    @property
    def status(self) -> ShipmentStatus:
        return ShipmentStatus.EN_VALIDACION


class IncompletoState(ShipmentState):
    """Validation found mismatches."""

    @property
    def status(self) -> ShipmentStatus:
        return ShipmentStatus.INCOMPLETO


class CompletoState(ShipmentState):
    """All fields validated."""

    @property
    def status(self) -> ShipmentStatus:
        return ShipmentStatus.COMPLETO


class NotificadoState(ShipmentState):
    """Client notified."""

    @property
    def status(self) -> ShipmentStatus:
        return ShipmentStatus.NOTIFICADO


class AprobadoClienteState(ShipmentState):
    """Client approved."""

    @property
    def status(self) -> ShipmentStatus:
        return ShipmentStatus.APROBADO_CLIENTE


class ConNovedadState(ShipmentState):
    """Novelty registered."""

    @property
    def status(self) -> ShipmentStatus:
        return ShipmentStatus.CON_NOVEDAD


class FinalizadoState(ShipmentState):
    """Workflow completed."""

    @property
    def status(self) -> ShipmentStatus:
        return ShipmentStatus.FINALIZADO


class RechazadoState(ShipmentState):
    """Rejected — terminal."""

    @property
    def status(self) -> ShipmentStatus:
        return ShipmentStatus.RECHAZADO


class ShipmentStateFactory:
    """Factory: maps ShipmentStatus enum to concrete State objects."""

    _MAP: dict[ShipmentStatus, type[ShipmentState]] = {
        ShipmentStatus.PENDIENTE_EXTRACCION: PendienteExtraccionState,
        ShipmentStatus.EXTRAIDO: ExtraidoState,
        ShipmentStatus.EN_DIGITACION: EnDigitacionState,
        ShipmentStatus.EN_VALIDACION: EnValidacionState,
        ShipmentStatus.INCOMPLETO: IncompletoState,
        ShipmentStatus.COMPLETO: CompletoState,
        ShipmentStatus.NOTIFICADO: NotificadoState,
        ShipmentStatus.APROBADO_CLIENTE: AprobadoClienteState,
        ShipmentStatus.CON_NOVEDAD: ConNovedadState,
        ShipmentStatus.FINALIZADO: FinalizadoState,
        ShipmentStatus.RECHAZADO: RechazadoState,
    }

    @classmethod
    def create(cls, status: ShipmentStatus) -> ShipmentState:
        """Instantiate state for the given status."""
        state_cls = cls._MAP.get(status)
        if state_cls is None:
            msg = f"Unknown status: {status}"
            raise InvalidStateTransitionError(msg)
        return state_cls()

    @classmethod
    def validate_transition(
        cls,
        current: ShipmentStatus,
        target: ShipmentStatus,
    ) -> ShipmentStatus:
        """Validate transition and return confirmed target status."""
        state = cls.create(current)
        new_state = state.transition_to(target)
        return new_state.status

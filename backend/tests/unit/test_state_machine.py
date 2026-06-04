"""State machine unit tests."""

import pytest

from app.domain.exceptions import InvalidStateTransitionError
from app.domain.state_machine.state import ShipmentStateFactory
from app.domain.value_objects.shipment_status import ShipmentStatus


def test_happy_path_transitions() -> None:
    """Valid forward transitions along the main workflow."""
    chain = [
        ShipmentStatus.PENDIENTE_EXTRACCION,
        ShipmentStatus.EXTRAIDO,
        ShipmentStatus.EN_DIGITACION,
        ShipmentStatus.EN_VALIDACION,
        ShipmentStatus.COMPLETO,
        ShipmentStatus.NOTIFICADO,
        ShipmentStatus.APROBADO_CLIENTE,
        ShipmentStatus.FINALIZADO,
    ]
    for current, target in zip(chain, chain[1:], strict=False):
        result = ShipmentStateFactory.validate_transition(current, target)
        assert result == target


def test_incompleto_loop() -> None:
    """INCOMPLETO can return to EN_VALIDACION."""
    ShipmentStateFactory.validate_transition(
        ShipmentStatus.EN_VALIDACION,
        ShipmentStatus.INCOMPLETO,
    )
    ShipmentStateFactory.validate_transition(
        ShipmentStatus.INCOMPLETO,
        ShipmentStatus.EN_VALIDACION,
    )


def test_reject_from_non_terminal() -> None:
    """Any non-terminal state may transition to RECHAZADO."""
    ShipmentStateFactory.validate_transition(
        ShipmentStatus.EN_DIGITACION,
        ShipmentStatus.RECHAZADO,
    )


def test_forbidden_transition_raises() -> None:
    """PENDIENTE_EXTRACCION cannot skip to COMPLETO."""
    with pytest.raises(InvalidStateTransitionError):
        ShipmentStateFactory.validate_transition(
            ShipmentStatus.PENDIENTE_EXTRACCION,
            ShipmentStatus.COMPLETO,
        )


def test_terminal_states_block_transitions() -> None:
    """FINALIZADO cannot transition further."""
    with pytest.raises(InvalidStateTransitionError):
        ShipmentStateFactory.validate_transition(
            ShipmentStatus.FINALIZADO,
            ShipmentStatus.EXTRAIDO,
        )

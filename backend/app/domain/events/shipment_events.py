"""Shipment domain events emitted on state transitions (Observer subject)."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID


@dataclass(frozen=True)
class DomainEvent:
    """Base domain event."""

    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(frozen=True)
class ShipmentCompletedEvent(DomainEvent):
    """Emitted when shipment reaches COMPLETO status."""

    shipment_id: UUID = field(default_factory=lambda: UUID(int=0))


@dataclass(frozen=True)
class ShipmentNotifiedEvent(DomainEvent):
    """Emitted when shipment reaches NOTIFICADO status."""

    shipment_id: UUID = field(default_factory=lambda: UUID(int=0))
    client_id: UUID = field(default_factory=lambda: UUID(int=0))


@dataclass(frozen=True)
class ShipmentApprovedEvent(DomainEvent):
    """Emitted when shipment reaches APROBADO_CLIENTE status."""

    shipment_id: UUID = field(default_factory=lambda: UUID(int=0))


@dataclass(frozen=True)
class ShipmentRejectedEvent(DomainEvent):
    """Emitted when shipment is RECHAZADO."""

    shipment_id: UUID = field(default_factory=lambda: UUID(int=0))
    reason: str = ""

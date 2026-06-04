"""Domain events for Observer pattern."""

from app.domain.events.shipment_events import (
    DomainEvent,
    ShipmentApprovedEvent,
    ShipmentCompletedEvent,
    ShipmentNotifiedEvent,
    ShipmentRejectedEvent,
)

__all__ = [
    "DomainEvent",
    "ShipmentApprovedEvent",
    "ShipmentCompletedEvent",
    "ShipmentNotifiedEvent",
    "ShipmentRejectedEvent",
]

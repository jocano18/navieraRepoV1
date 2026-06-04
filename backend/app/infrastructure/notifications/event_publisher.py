"""LoggingEventPublisher — Observer dispatch for domain events."""

import logging

from app.application.ports.event_publisher import EventPublisher
from app.domain.events.shipment_events import (
    DomainEvent,
    ShipmentCompletedEvent,
    ShipmentNotifiedEvent,
)

logger = logging.getLogger(__name__)


class LoggingEventPublisher(EventPublisher):
    """Observer publisher that logs domain events (extensible to webhooks)."""

    async def publish(self, event: DomainEvent) -> None:
        """Dispatch event to subscribers."""
        if isinstance(event, ShipmentCompletedEvent):
            logger.info("EVENT ShipmentCompleted id=%s", event.shipment_id)
        elif isinstance(event, ShipmentNotifiedEvent):
            logger.info(
                "EVENT ShipmentNotified id=%s client=%s",
                event.shipment_id,
                event.client_id,
            )
        else:
            logger.info("EVENT %s", type(event).__name__)

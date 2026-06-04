"""Domain event publisher port (Observer pattern)."""

from abc import ABC, abstractmethod

from app.domain.events.shipment_events import DomainEvent


class EventPublisher(ABC):
    """Port for publishing domain events to subscribers."""

    @abstractmethod
    async def publish(self, event: DomainEvent) -> None:
        """Dispatch a domain event to all registered observers."""

"""Notification observer interface (Observer pattern)."""

from abc import ABC, abstractmethod
from uuid import UUID


class NotificationObserver(ABC):
    """Observer that reacts to notification events.

    Subscribers implement this interface to receive callbacks when
    notifications are dispatched (e.g., audit logging, webhooks).
    """

    @abstractmethod
    async def on_notification_sent(
        self,
        client_id: UUID,
        subject: str,
        *,
        shipment_id: UUID | None = None,
    ) -> None:
        """Handle a notification-sent event.

        Args:
            client_id: Recipient client identifier.
            subject: Notification subject line.
            shipment_id: Optional related shipment identifier.
        """


class NotificationSubject:
    """Subject that maintains and notifies Observer subscribers."""

    def __init__(self) -> None:
        """Initialize with an empty observer list."""
        self._observers: list[NotificationObserver] = []

    def attach(self, observer: NotificationObserver) -> None:
        """Register an observer.

        Args:
            observer: Observer to attach.
        """
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: NotificationObserver) -> None:
        """Remove an observer.

        Args:
            observer: Observer to detach.
        """
        self._observers.remove(observer)

    async def notify_observers(
        self,
        client_id: UUID,
        subject: str,
        *,
        shipment_id: UUID | None = None,
    ) -> None:
        """Notify all attached observers of a sent notification.

        Args:
            client_id: Recipient client identifier.
            subject: Notification subject line.
            shipment_id: Optional related shipment identifier.
        """
        for observer in self._observers:
            await observer.on_notification_sent(
                client_id,
                subject,
                shipment_id=shipment_id,
            )

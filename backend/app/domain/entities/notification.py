"""Notification entity."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID


class NotificationType(str, Enum):
    """Category of client notification."""

    SHIPMENT_READY = "SHIPMENT_READY"
    NOVELTY_REGISTERED = "NOVELTY_REGISTERED"
    APPROVAL_REQUEST = "APPROVAL_REQUEST"
    REJECTION = "REJECTION"


class NotificationStatus(str, Enum):
    """Delivery status of a notification."""

    PENDING = "PENDING"
    SENT = "SENT"
    FAILED = "FAILED"


@dataclass
class Notification:
    """Record of a notification dispatched to a client."""

    id: UUID
    shipment_id: UUID
    notification_type: NotificationType
    recipient: str
    subject: str
    body: str
    status: NotificationStatus = NotificationStatus.PENDING
    sent_at: datetime | None = None

"""Domain entities."""

from app.domain.entities.client import Client
from app.domain.entities.container import Container
from app.domain.entities.digitized_data import DigitizedData
from app.domain.entities.document_data import DocumentData
from app.domain.entities.mbl import HBL, MBL
from app.domain.entities.notification import (
    Notification,
    NotificationStatus,
    NotificationType,
)
from app.domain.entities.shipment import Shipment
from app.domain.entities.validation_result import FieldComparison, ValidationResult

__all__ = [
    "Client",
    "Container",
    "DigitizedData",
    "DocumentData",
    "FieldComparison",
    "HBL",
    "MBL",
    "Notification",
    "NotificationStatus",
    "NotificationType",
    "Shipment",
    "ValidationResult",
]

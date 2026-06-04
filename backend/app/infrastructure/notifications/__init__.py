"""Notification adapters."""

from app.infrastructure.notifications.email_notifier import EmailNotifier
from app.infrastructure.notifications.observer import NotificationObserver

__all__ = ["EmailNotifier", "NotificationObserver"]

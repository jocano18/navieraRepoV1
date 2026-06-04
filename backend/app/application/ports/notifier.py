"""Notifier port (Observer pattern — email adapter)."""

from abc import ABC, abstractmethod
from pathlib import Path
from uuid import UUID


class Notifier(ABC):
    """Port for dispatching notifications with optional PDF attachments."""

    @abstractmethod
    async def notify(
        self,
        recipient_email: str,
        subject: str,
        body: str,
        *,
        attachment_path: Path | None = None,
        shipment_id: UUID | None = None,
    ) -> None:
        """Send notification email."""

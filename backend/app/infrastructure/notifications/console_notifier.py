"""ConsoleNotifier — dev/test fake for Notifier port."""

import logging
from pathlib import Path
from uuid import UUID

from app.application.ports.notifier import Notifier

logger = logging.getLogger(__name__)


class ConsoleNotifier(Notifier):
    """Fake notifier that logs emails to stdout (tests and local dev)."""

    async def notify(
        self,
        recipient_email: str,
        subject: str,
        body: str,
        *,
        attachment_path: Path | None = None,
        shipment_id: UUID | None = None,
    ) -> None:
        """Log notification instead of sending SMTP."""
        logger.info(
            "NOTIFY to=%s subject=%s shipment=%s attachment=%s\n%s",
            recipient_email,
            subject,
            shipment_id,
            attachment_path,
            body,
        )

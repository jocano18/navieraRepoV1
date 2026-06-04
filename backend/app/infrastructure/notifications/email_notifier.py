"""EmailNotifier — SMTP adapter with PDF attachment support."""

import logging
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from uuid import UUID

import aiosmtplib

from app.application.ports.notifier import Notifier
from app.infrastructure.config.settings import Settings

logger = logging.getLogger(__name__)


class EmailNotifier(Notifier):
    """Adapter: sends email via aiosmtplib (MailHog in development)."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    async def notify(
        self,
        recipient_email: str,
        subject: str,
        body: str,
        *,
        attachment_path: Path | None = None,
        shipment_id: UUID | None = None,
    ) -> None:
        """Send email with optional PDF attachment."""
        message = MIMEMultipart()
        message["From"] = self._settings.smtp_from
        message["To"] = recipient_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain", "utf-8"))

        if attachment_path and attachment_path.exists():
            pdf_bytes = attachment_path.read_bytes()
            part = MIMEApplication(pdf_bytes, _subtype="pdf")
            part.add_header(
                "Content-Disposition",
                "attachment",
                filename=attachment_path.name,
            )
            message.attach(part)

        try:
            await aiosmtplib.send(
                message,
                hostname=self._settings.smtp_host,
                port=self._settings.smtp_port,
                username=self._settings.smtp_user or None,
                password=self._settings.smtp_password or None,
                use_tls=self._settings.smtp_use_tls,
            )
        except Exception:
            logger.exception("Failed to send email to %s", recipient_email)
            raise

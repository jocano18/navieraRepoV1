"""Signed approval tokens for email deep links."""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import time
from uuid import UUID

from app.domain.exceptions import InvalidApprovalTokenError
from app.infrastructure.config.settings import Settings


class ApprovalTokenService:
    """Create and verify HMAC-signed tokens bound to a shipment id."""

    def __init__(self, settings: Settings) -> None:
        self._secret = settings.approval_token_secret.encode("utf-8")
        self._max_age_seconds = settings.approval_token_max_age_days * 86400
        self._public_api_url = settings.public_api_url.rstrip("/")

    def create(self, shipment_id: UUID) -> str:
        """Build a URL-safe token for the given shipment."""
        payload = {
            "sid": str(shipment_id),
            "exp": int(time.time()) + self._max_age_seconds,
        }
        payload_b64 = _b64_encode(json.dumps(payload, separators=(",", ":")).encode())
        sig = hmac.new(self._secret, payload_b64.encode("ascii"), hashlib.sha256).digest()
        sig_b64 = _b64_encode(sig)
        return f"{payload_b64}.{sig_b64}"

    def verify(self, token: str) -> UUID:
        """Validate token and return shipment id."""
        try:
            payload_b64, sig_b64 = token.split(".", 1)
        except ValueError as exc:
            raise InvalidApprovalTokenError("Enlace de aprobación inválido.") from exc

        expected_sig = hmac.new(
            self._secret,
            payload_b64.encode("ascii"),
            hashlib.sha256,
        ).digest()
        try:
            provided_sig = _b64_decode(sig_b64)
        except ValueError as exc:
            raise InvalidApprovalTokenError("Enlace de aprobación inválido.") from exc

        if not hmac.compare_digest(expected_sig, provided_sig):
            raise InvalidApprovalTokenError("Enlace de aprobación inválido.")

        try:
            payload = json.loads(_b64_decode(payload_b64))
            shipment_id = UUID(payload["sid"])
            exp = int(payload["exp"])
        except (KeyError, ValueError, TypeError) as exc:
            raise InvalidApprovalTokenError("Enlace de aprobación inválido.") from exc

        if time.time() > exp:
            raise InvalidApprovalTokenError("El enlace de aprobación ha expirado.")

        return shipment_id

    def build_approval_url(self, shipment_id: UUID) -> str:
        """Full URL for the approve button in notification emails."""
        token = self.create(shipment_id)
        return f"{self._public_api_url}/public/approve?token={token}"


def _b64_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def _b64_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)

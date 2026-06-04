"""Unit tests for email approval tokens."""

from uuid import UUID

import pytest

from app.domain.exceptions import InvalidApprovalTokenError
from app.infrastructure.config.settings import Settings
from app.infrastructure.notifications.approval_token import ApprovalTokenService

SHIPMENT_ID = UUID("11111111-1111-1111-1111-111111111111")


@pytest.fixture
def token_service() -> ApprovalTokenService:
    settings = Settings(
        PUBLIC_API_URL="http://localhost:8000",
        APPROVAL_TOKEN_SECRET="test-secret",
        APPROVAL_TOKEN_MAX_AGE_DAYS=7,
    )
    return ApprovalTokenService(settings)


def test_create_and_verify_roundtrip(token_service: ApprovalTokenService) -> None:
    token = token_service.create(SHIPMENT_ID)
    assert token_service.verify(token) == SHIPMENT_ID


def test_build_approval_url(token_service: ApprovalTokenService) -> None:
    url = token_service.build_approval_url(SHIPMENT_ID)
    assert url.startswith("http://localhost:8000/public/approve?token=")


def test_tampered_token_rejected(token_service: ApprovalTokenService) -> None:
    token = token_service.create(SHIPMENT_ID)
    bad = token[:-1] + ("a" if token[-1] != "a" else "b")
    with pytest.raises(InvalidApprovalTokenError):
        token_service.verify(bad)

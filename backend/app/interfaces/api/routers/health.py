"""Health check router."""

from typing import Any

from fastapi import APIRouter
from sqlalchemy import text

from app.infrastructure.config.settings import get_settings
from app.infrastructure.persistence.session import get_session_factory

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check() -> dict[str, str]:
    """Return application health status.

    Returns:
        JSON object with status key set to 'ok'.
    """
    return {"status": "ok"}


async def _check_database() -> str:
    """Ping the configured database with a trivial query."""
    try:
        factory = get_session_factory()
        async with factory() as session:
            await session.execute(text("SELECT 1"))
        return "ok"
    except Exception:
        return "error"


@router.get("/health/detailed", include_in_schema=False)
async def health_check_detailed() -> dict[str, Any]:
    """Return detailed health including database connectivity.

    Returns:
        Extended health payload including dependency checks.
    """
    settings = get_settings()
    db_status = await _check_database()
    smtp_status = "skipped" if settings.use_console_notifier else "not_checked"
    overall = "ok" if db_status == "ok" else "degraded"
    return {
        "status": overall,
        "database": db_status,
        "smtp": smtp_status,
    }

"""Database seed data for development."""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.client import Client
from app.infrastructure.persistence.mappers import client_to_model
from app.infrastructure.persistence.models import ClientModel

DEFAULT_CLIENT_ID = UUID("00000000-0000-0000-0000-000000000001")


async def seed_default_client(session: AsyncSession) -> None:
    """Insert default client if not present."""
    result = await session.get(ClientModel, str(DEFAULT_CLIENT_ID))
    if result is not None:
        return
    client = Client(
        id=DEFAULT_CLIENT_ID,
        name="Demo Import Client",
        nit="900123456-1",
        email="client@naviera.local",
    )
    session.add(client_to_model(client))
    await session.commit()

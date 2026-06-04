"""SQLAlchemy ClientRepository."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.client_repository import ClientRepository
from app.domain.entities.client import Client
from app.infrastructure.persistence.mappers import client_to_domain, client_to_model
from app.infrastructure.persistence.models import ClientModel


class SqlAlchemyClientRepository(ClientRepository):
    """Client persistence adapter."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, client_id: UUID) -> Client | None:
        model = await self._session.get(ClientModel, str(client_id))
        if model is None:
            return None
        return client_to_domain(model)

    async def list_all(self) -> list[Client]:
        result = await self._session.execute(select(ClientModel))
        return [client_to_domain(row) for row in result.scalars().all()]

    async def save(self, client: Client) -> Client:
        existing = await self._session.get(ClientModel, str(client.id))
        if existing is None:
            self._session.add(client_to_model(client))
        else:
            existing.name = client.name
            existing.nit = client.nit
            existing.email = client.email
            existing.is_active = client.is_active
        await self._session.commit()
        return client

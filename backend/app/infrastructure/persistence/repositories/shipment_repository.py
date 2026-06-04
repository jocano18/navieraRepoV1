"""SQLAlchemy ShipmentRepository (Repository pattern)."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.shipment_repository import ShipmentRepository
from app.domain.entities.shipment import Shipment
from app.domain.value_objects.shipment_status import ShipmentStatus
from app.infrastructure.persistence.mappers import shipment_to_domain, shipment_to_model
from app.infrastructure.persistence.models import ShipmentModel


class SqlAlchemyShipmentRepository(ShipmentRepository):
    """Persist Shipment aggregates via SQLAlchemy async session."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, shipment_id: UUID) -> Shipment | None:
        result = await self._session.get(ShipmentModel, str(shipment_id))
        if result is None:
            return None
        return shipment_to_domain(result)

    async def save(self, shipment: Shipment) -> Shipment:
        existing = await self._session.get(ShipmentModel, str(shipment.id))
        model = shipment_to_model(shipment, existing)
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return shipment_to_domain(model)

    async def list_all(
        self,
        *,
        status: ShipmentStatus | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Shipment]:
        stmt = select(ShipmentModel).offset(skip).limit(limit)
        if status is not None:
            stmt = stmt.where(ShipmentModel.status == status.value)
        result = await self._session.execute(stmt)
        return [shipment_to_domain(row) for row in result.scalars().all()]

    async def delete(self, shipment_id: UUID) -> bool:
        model = await self._session.get(ShipmentModel, str(shipment_id))
        if model is None:
            return False
        await self._session.delete(model)
        await self._session.commit()
        return True

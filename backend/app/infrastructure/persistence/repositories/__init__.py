"""SQLAlchemy repository implementations."""

from app.infrastructure.persistence.repositories.shipment_repository import (
    SqlAlchemyShipmentRepository,
)

__all__ = ["SqlAlchemyShipmentRepository"]

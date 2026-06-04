"""SQLAlchemy ORM models (infrastructure only — mapped to domain via mappers)."""

from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Declarative base for ORM models."""


class ClientModel(Base):
    """Client table."""

    __tablename__ = "clients"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    nit: Mapped[str] = mapped_column(String(50), default="")
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class ShipmentModel(Base):
    """Shipment aggregate persistence."""

    __tablename__ = "shipments"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    reference: Mapped[str] = mapped_column(String(255), nullable=False)
    source_pdf_filename: Mapped[str] = mapped_column(String(512), nullable=False)
    cargo_type: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    client_id: Mapped[str] = mapped_column(String(36), ForeignKey("clients.id"))
    extracted_data_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    digitized_data_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    validation_result_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    novelty_description: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(UTC).replace(tzinfo=None),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(UTC).replace(tzinfo=None),
        onupdate=lambda: datetime.now(UTC).replace(tzinfo=None),
    )

    client: Mapped[ClientModel] = relationship("ClientModel")

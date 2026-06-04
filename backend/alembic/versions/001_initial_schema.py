"""Initial schema

Revision ID: 001
Revises:
Create Date: 2026-06-03

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create clients and shipments tables."""
    op.create_table(
        "clients",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("nit", sa.String(50), server_default=""),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default="1"),
    )
    op.create_table(
        "shipments",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("reference", sa.String(255), nullable=False),
        sa.Column("source_pdf_filename", sa.String(512), nullable=False),
        sa.Column("cargo_type", sa.String(20), nullable=False),
        sa.Column("status", sa.String(50), nullable=False),
        sa.Column("client_id", sa.String(36), sa.ForeignKey("clients.id")),
        sa.Column("extracted_data_json", sa.Text(), nullable=True),
        sa.Column("digitized_data_json", sa.Text(), nullable=True),
        sa.Column("validation_result_json", sa.Text(), nullable=True),
        sa.Column("novelty_description", sa.Text(), server_default=""),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    """Drop tables."""
    op.drop_table("shipments")
    op.drop_table("clients")

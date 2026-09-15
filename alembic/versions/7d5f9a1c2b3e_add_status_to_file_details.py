"""add upload status to file details

Revision ID: 7d5f9a1c2b3e
Revises: 1fbf784ae007
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "7d5f9a1c2b3e"
down_revision: Union[str, Sequence[str], None] = "1fbf784ae007"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "file_details",
        sa.Column("status", sa.String(), nullable=False, server_default="queued"),
    )
    op.alter_column("file_details", "status", server_default=None)


def downgrade() -> None:
    op.drop_column("file_details", "status")




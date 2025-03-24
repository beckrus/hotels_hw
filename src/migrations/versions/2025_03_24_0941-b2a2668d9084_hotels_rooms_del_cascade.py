"""hotels rooms del cascade

Revision ID: b2a2668d9084
Revises: 52f5c2a7db59
Create Date: 2025-03-24 09:41:53.866193

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa  # noqa F401


revision: str = "b2a2668d9084"
down_revision: Union[str, None] = "52f5c2a7db59"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint("rooms_hotel_id_fkey", "rooms", type_="foreignkey")
    op.create_foreign_key(
        None, "rooms", "hotels", ["hotel_id"], ["id"], ondelete="CASCADE"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "rooms", type_="foreignkey")
    op.create_foreign_key(
        "rooms_hotel_id_fkey", "rooms", "hotels", ["hotel_id"], ["id"]
    )

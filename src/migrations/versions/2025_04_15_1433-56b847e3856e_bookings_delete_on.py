"""bookings delete on

Revision ID: 56b847e3856e
Revises: fc642cb5f555
Create Date: 2025-04-15 14:33:05.974532

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "56b847e3856e"
down_revision: Union[str, None] = "fc642cb5f555"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint("bookings_user_id_fkey", "bookings", type_="foreignkey")
    op.drop_constraint("bookings_room_id_fkey", "bookings", type_="foreignkey")
    op.create_foreign_key(
        None, "bookings", "users", ["user_id"], ["id"], ondelete="CASCADE"
    )
    op.create_foreign_key(
        None, "bookings", "rooms", ["room_id"], ["id"], ondelete="CASCADE"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "bookings", type_="foreignkey")
    op.drop_constraint(None, "bookings", type_="foreignkey")
    op.create_foreign_key(
        "bookings_room_id_fkey", "bookings", "rooms", ["room_id"], ["id"]
    )
    op.create_foreign_key(
        "bookings_user_id_fkey", "bookings", "users", ["user_id"], ["id"]
    )

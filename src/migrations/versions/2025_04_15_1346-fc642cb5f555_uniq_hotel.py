"""uniq_hotel

Revision ID: fc642cb5f555
Revises: 8022eb5c932e
Create Date: 2025-04-15 13:46:21.277346

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "fc642cb5f555"
down_revision: Union[str, None] = "8022eb5c932e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint("unique_hotel", "hotels", ["title", "location"])
    op.create_unique_constraint(None, "hotels", ["title"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "hotels", type_="unique")
    op.drop_constraint("unique_hotel", "hotels", type_="unique")

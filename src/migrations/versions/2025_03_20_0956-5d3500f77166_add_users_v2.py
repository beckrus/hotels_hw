"""add users_v2

Revision ID: 5d3500f77166
Revises: f8ff5acfd59a
Create Date: 2025-03-20 09:56:36.985334

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5d3500f77166"
down_revision: Union[str, None] = "f8ff5acfd59a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(None, "users", ["phone"])
    op.create_unique_constraint(None, "users", ["username"])
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "users", type_="unique")
    op.drop_constraint(None, "users", type_="unique")
    op.drop_constraint(None, "users", type_="unique")

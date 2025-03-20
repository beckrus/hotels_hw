"""add users_v3

Revision ID: 65bb51194962
Revises: 5d3500f77166
Create Date: 2025-03-20 12:07:26.955738

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "65bb51194962"
down_revision: Union[str, None] = "5d3500f77166"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "users", "email", existing_type=sa.VARCHAR(length=200), nullable=True
    )
    op.alter_column(
        "users", "phone", existing_type=sa.VARCHAR(length=200), nullable=True
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "users", "phone", existing_type=sa.VARCHAR(length=200), nullable=False
    )
    op.alter_column(
        "users", "email", existing_type=sa.VARCHAR(length=200), nullable=False
    )

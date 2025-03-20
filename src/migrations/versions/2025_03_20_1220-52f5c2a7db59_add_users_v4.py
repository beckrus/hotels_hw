"""add users_v4

Revision ID: 52f5c2a7db59
Revises: 65bb51194962
Create Date: 2025-03-20 12:20:39.889150

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "52f5c2a7db59"
down_revision: Union[str, None] = "65bb51194962"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "users", "first_name", existing_type=sa.VARCHAR(length=200), nullable=True
    )
    op.alter_column(
        "users", "last_name", existing_type=sa.VARCHAR(length=200), nullable=True
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "users", "last_name", existing_type=sa.VARCHAR(length=200), nullable=False
    )
    op.alter_column(
        "users", "first_name", existing_type=sa.VARCHAR(length=200), nullable=False
    )

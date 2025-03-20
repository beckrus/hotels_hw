"""add users

Revision ID: 44ce3fa491fc
Revises: 37402ca20d54
Create Date: 2025-03-20 09:27:01.857582

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "44ce3fa491fc"
down_revision: Union[str, None] = "37402ca20d54"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("phone", sa.String(length=200), nullable=False),
        sa.Column("password_hash", sa.String(length=200), nullable=False),
        sa.Column("is_varified", sa.Boolean(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_superuser", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")

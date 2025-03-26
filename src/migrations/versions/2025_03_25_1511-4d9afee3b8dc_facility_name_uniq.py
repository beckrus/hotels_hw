"""facility name uniq

Revision ID: 4d9afee3b8dc
Revises: 01d4594fc368
Create Date: 2025-03-25 15:11:44.427990

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa  # noqa F401


# revision identifiers, used by Alembic.
revision: str = "4d9afee3b8dc"
down_revision: Union[str, None] = "01d4594fc368"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(None, "facilities", ["name"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "facilities", type_="unique")

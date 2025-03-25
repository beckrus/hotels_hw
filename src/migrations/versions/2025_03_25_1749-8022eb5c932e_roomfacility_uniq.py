"""roomfacility uniq

Revision ID: 8022eb5c932e
Revises: 4d9afee3b8dc
Create Date: 2025-03-25 17:49:31.186896

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8022eb5c932e"
down_revision: Union[str, None] = "4d9afee3b8dc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(
        "_rooms_facilities", "rooms_facilities", ["room_id", "facility_id"]
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("_rooms_facilities", "rooms_facilities", type_="unique")

"""unique facility_id and room_id for RoomFacilitiesRepository

Revision ID: 0d5857d9c8ec
Revises: 800a34ded968
Create Date: 2025-12-08 14:07:17.023332

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0d5857d9c8ec"
down_revision: Union[str, Sequence[str], None] = "800a34ded968"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(
        "uix_room_facility", "room_facilities", ["room_id", "facility_id"]
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("uix_room_facility", "room_facilities", type_="unique")

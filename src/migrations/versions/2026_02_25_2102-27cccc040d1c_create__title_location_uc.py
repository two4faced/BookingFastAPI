"""create _title_location_uc

Revision ID: 27cccc040d1c
Revises: ded943d3bf4e
Create Date: 2026-02-25 21:02:53.068528

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '27cccc040d1c'
down_revision: Union[str, Sequence[str], None] = 'ded943d3bf4e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint('_title_location_uc', 'hotels', ['title', 'location'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('_title_location_uc', 'hotels', type_='unique')

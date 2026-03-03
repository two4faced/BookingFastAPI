"""add guests count for rooms

Revision ID: 2a6be92157d3
Revises: 047141d716c7
Create Date: 2026-03-03 14:51:42.104285

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2a6be92157d3'
down_revision: Union[str, Sequence[str], None] = '047141d716c7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('rooms', sa.Column('guests_count', sa.Integer(), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('rooms', 'guests_count')

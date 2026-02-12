"""change rating_text type

Revision ID: f89122bea7a6
Revises: 5d04563dfbee
Create Date: 2026-02-12 09:09:56.409973

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f89122bea7a6'
down_revision: Union[str, Sequence[str], None] = '5d04563dfbee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        'ratings',
        'rating_text',
        existing_type=sa.TEXT(),
        type_=sa.VARCHAR(length=1000),
        existing_nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        'ratings',
        'rating_text',
        existing_type=sa.VARCHAR(length=1000),
        type_=sa.TEXT(),
        existing_nullable=False,
    )

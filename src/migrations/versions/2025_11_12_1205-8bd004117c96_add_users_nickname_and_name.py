"""add users nickname and name

Revision ID: 8bd004117c96
Revises: 8bb61d1ddab5
Create Date: 2025-11-12 12:05:51.733003

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8bd004117c96'
down_revision: Union[str, Sequence[str], None] = '8bb61d1ddab5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('name', sa.String(length=100), nullable=False))
    op.add_column('users', sa.Column('nickname', sa.String(length=50), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'nickname')
    op.drop_column('users', 'name')

"""add stars and rating for hotels

Revision ID: 5c270dfdb28c
Revises: 2a6be92157d3
Create Date: 2026-03-03 15:03:24.197058

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5c270dfdb28c"
down_revision: Union[str, Sequence[str], None] = "2a6be92157d3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("hotels", sa.Column("stars", sa.Integer(), nullable=False))
    op.add_column("hotels", sa.Column("rating", sa.Float(), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("hotels", "rating")
    op.drop_column("hotels", "stars")

"""add ratings

Revision ID: 5d04563dfbee
Revises: 0d5857d9c8ec
Create Date: 2026-02-08 09:27:49.031490

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '5d04563dfbee'
down_revision: Union[str, Sequence[str], None] = '0d5857d9c8ec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'ratings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('hotel_id', sa.Integer(), nullable=False),
        sa.Column('rating', sa.Integer(), nullable=False),
        sa.Column('rating_text', sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ['hotel_id'],
            ['hotels.id'],
        ),
        sa.ForeignKeyConstraint(
            ['user_id'],
            ['users.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('ratings')

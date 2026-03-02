"""make facilities unique

Revision ID: 047141d716c7
Revises: 27cccc040d1c
Create Date: 2026-02-27 10:53:48.038206

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '047141d716c7'
down_revision: Union[str, Sequence[str], None] = '27cccc040d1c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(None, 'facilities', ['title'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, 'facilities', type_='unique')

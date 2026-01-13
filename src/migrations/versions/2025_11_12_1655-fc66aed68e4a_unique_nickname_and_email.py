"""unique nickname and email

Revision ID: fc66aed68e4a
Revises: 8bd004117c96
Create Date: 2025-11-12 16:55:14.033783

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'fc66aed68e4a'
down_revision: Union[str, Sequence[str], None] = '8bd004117c96'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(None, 'users', ['email'])
    op.create_unique_constraint(None, 'users', ['nickname'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, 'users', type_='unique')  # type: ignore
    op.drop_constraint(None, 'users', type_='unique')  # type: ignore

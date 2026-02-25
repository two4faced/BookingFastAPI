"""delete nicknames from users

Revision ID: ded943d3bf4e
Revises: f89122bea7a6
Create Date: 2026-02-25 15:19:42.693406

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ded943d3bf4e"
down_revision: Union[str, Sequence[str], None] = "f89122bea7a6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint(op.f("users_nickname_key"), "users", type_="unique")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "users",
        sa.Column(
            "nickname", sa.VARCHAR(length=50), autoincrement=False, nullable=False
        ),
    )
    op.create_unique_constraint(
        op.f("users_nickname_key"),
        "users",
        ["nickname"],
        postgresql_nulls_not_distinct=False,
    )

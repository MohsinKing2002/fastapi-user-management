"""create users table

Revision ID: 91633342cf5a
Revises:
Create Date: 2026-10-18 12:23:15.341159

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "91633342cf5a"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # create users table
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=150), unique=True, nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )

    # create indexes
    op.create_index("ix_users_id", "users", ["id"], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    # drop table and indexes
    op.drop_index("ix_users_id", table_name="users")
    op.drop_table("users")

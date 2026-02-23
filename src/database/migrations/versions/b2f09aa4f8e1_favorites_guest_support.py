"""favorites guest support with session and soft-delete

Revision ID: b2f09aa4f8e1
Revises: 97461bcf8c77
Create Date: 2026-02-14
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "b2f09aa4f8e1"
down_revision: Union[str, None] = "97461bcf8c77"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("favorites_id_fkey", "favorites", type_="foreignkey")

    op.add_column(
        "favorites", sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=True)
    )
    op.add_column("favorites", sa.Column("session_id", sa.String(length=64), nullable=True))
    op.add_column(
        "favorites",
        sa.Column(
            "is_deleted", sa.Boolean(), nullable=False, server_default=sa.text("false")
        ),
    )
    op.add_column("favorites", sa.Column("deleted_at", sa.DateTime(), nullable=True))
    op.add_column(
        "favorites",
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )

    op.execute("UPDATE favorites SET user_id = id")

    op.create_foreign_key(
        "favorites_user_id_fkey",
        "favorites",
        "users",
        ["user_id"],
        ["id"],
    )
    op.create_index("ix_favorites_user_id", "favorites", ["user_id"], unique=False)
    op.create_index(
        "uq_active_favorites_user",
        "favorites",
        ["user_id"],
        unique=True,
        postgresql_where=sa.text("is_deleted = false"),
    )
    op.create_index("ix_favorites_session_id", "favorites", ["session_id"], unique=False)
    op.create_index(
        "uq_active_favorites_session",
        "favorites",
        ["session_id"],
        unique=True,
        postgresql_where=sa.text("is_deleted = false"),
    )

    op.create_unique_constraint(
        "uq_favorite_product", "favorites_products", ["favorite_id", "product_id"]
    )


def downgrade() -> None:
    op.drop_constraint("uq_favorite_product", "favorites_products", type_="unique")

    op.drop_index("uq_active_favorites_session", table_name="favorites")
    op.drop_index("ix_favorites_session_id", table_name="favorites")
    op.drop_index("uq_active_favorites_user", table_name="favorites")
    op.drop_index("ix_favorites_user_id", table_name="favorites")
    op.drop_constraint("favorites_user_id_fkey", "favorites", type_="foreignkey")

    # Best-effort data downgrade: keep only user-linked favorites and restore 1:1 id->user_id
    op.execute("DELETE FROM favorites_products fp USING favorites f WHERE fp.favorite_id = f.id AND f.user_id IS NULL")
    op.execute("DELETE FROM favorites WHERE user_id IS NULL")
    op.execute("UPDATE favorites SET id = user_id WHERE user_id IS NOT NULL")

    op.drop_column("favorites", "created_at")
    op.drop_column("favorites", "deleted_at")
    op.drop_column("favorites", "is_deleted")
    op.drop_column("favorites", "session_id")
    op.drop_column("favorites", "user_id")

    op.create_foreign_key("favorites_id_fkey", "favorites", "users", ["id"], ["id"])

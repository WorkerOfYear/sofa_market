"""add i18n locale columns (name_ru, name_kk, etc.)

Revision ID: g9b0c1d2e3f4
Revises: f8a9b0c1d2e3
Create Date: 2025-02-14

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "g9b0c1d2e3f4"
down_revision: Union[str, None] = "f8a9b0c1d2e3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "products",
        sa.Column("name_ru", sa.String(length=256), nullable=True),
    )
    op.add_column(
        "products",
        sa.Column("name_kk", sa.String(length=256), nullable=True),
    )
    op.add_column(
        "products",
        sa.Column("description_ru", sa.String(length=256), nullable=True),
    )
    op.add_column(
        "products",
        sa.Column("description_kk", sa.String(length=256), nullable=True),
    )
    op.add_column(
        "categories",
        sa.Column("name_ru", sa.String(length=256), nullable=True),
    )
    op.add_column(
        "categories",
        sa.Column("name_kk", sa.String(length=256), nullable=True),
    )
    op.execute(
        "UPDATE products SET name_ru = name, description_ru = description"
    )
    op.execute("UPDATE categories SET name_ru = name")


def downgrade() -> None:
    op.drop_column("products", "description_kk")
    op.drop_column("products", "description_ru")
    op.drop_column("products", "name_kk")
    op.drop_column("products", "name_ru")
    op.drop_column("categories", "name_kk")
    op.drop_column("categories", "name_ru")

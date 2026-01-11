"""add image storage type enum

Revision ID: e7f7a38eafd0
Revises: 4d88c24cccee
Create Date: 2025-12-30 12:55:25.916339

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'e7f7a38eafd0'
down_revision: Union[str, None] = '4d88c24cccee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('images', sa.Column('storage_type', sa.Enum('LOCAL', 'S3', 'YANDEX', name='imagestoragetypeenum', native_enum=False), nullable=False))


def downgrade() -> None:
    op.drop_column('images', 'storage_type')

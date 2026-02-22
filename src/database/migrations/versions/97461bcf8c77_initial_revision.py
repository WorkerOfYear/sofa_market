"""initial revision

Revision ID: 97461bcf8c77
Revises: 
Create Date: 2026-02-22 19:56:43.997901

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '97461bcf8c77'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=False),
    sa.Column('name_ru', sa.String(length=256), nullable=True),
    sa.Column('name_kk', sa.String(length=256), nullable=True),
    sa.Column('slug', sa.String(length=256), nullable=False),
    sa.Column('created_at', sa.Date(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('promotions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=False),
    sa.Column('discount_percent', sa.Integer(), nullable=False),
    sa.Column('valid_from', sa.DateTime(), nullable=True),
    sa.Column('valid_until', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('stores',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('city', sa.String(length=100), nullable=False),
    sa.Column('address', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=400), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('textile',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('producer', sa.String(length=256), nullable=False),
    sa.Column('color', sa.String(length=256), nullable=False),
    sa.Column('description', sa.String(length=512), nullable=False),
    sa.Column('is_available', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('email', sa.String(length=320), nullable=True),
    sa.Column('hashed_password', sa.String(length=128), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.Column('first_name', sa.String(length=256), nullable=True),
    sa.Column('last_name', sa.String(length=256), nullable=True),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('city', sa.String(length=128), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=False)
    op.create_index(op.f('ix_users_phone'), 'users', ['phone'], unique=True)
    op.create_table('carts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.Column('session_id', sa.String(length=64), nullable=True),
    sa.Column('total_price', sa.Integer(), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_carts_session_id'), 'carts', ['session_id'], unique=False)
    op.create_index(op.f('ix_carts_user_id'), 'carts', ['user_id'], unique=False)
    op.create_table('favorites',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=False),
    sa.Column('name_ru', sa.String(length=256), nullable=True),
    sa.Column('name_kk', sa.String(length=256), nullable=True),
    sa.Column('slug', sa.String(length=256), nullable=False),
    sa.Column('description', sa.String(length=256), nullable=False),
    sa.Column('description_ru', sa.String(length=256), nullable=True),
    sa.Column('description_kk', sa.String(length=256), nullable=True),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('purchases',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('CREATED', 'PROCESSED', name='purchasestatusenum'), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('is_user_deleted', sa.Boolean(), nullable=False),
    sa.Column('user_deleted_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('carts_products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cart_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cart_id'], ['carts.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dimensions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('height', sa.String(length=10), nullable=False),
    sa.Column('width', sa.String(length=10), nullable=False),
    sa.Column('depth', sa.String(length=10), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favorites_products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('favorite_id', sa.UUID(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['favorite_id'], ['favorites.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('images',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('storage_type', sa.Enum('LOCAL', 'S3', 'YANDEX', name='imagestoragetypeenum', native_enum=False), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('promotions_products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('promotion_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['promotion_id'], ['promotions.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('promotion_id', 'product_id', name='uq_promotion_product')
    )
    op.create_table('purchases_products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('purchase_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['purchase_id'], ['purchases.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('purchases_products')
    op.drop_table('promotions_products')
    op.drop_table('images')
    op.drop_table('favorites_products')
    op.drop_table('dimensions')
    op.drop_table('carts_products')
    op.drop_table('purchases')
    op.drop_table('products')
    op.drop_table('favorites')
    op.drop_index(op.f('ix_carts_user_id'), table_name='carts')
    op.drop_index(op.f('ix_carts_session_id'), table_name='carts')
    op.drop_table('carts')
    op.drop_index(op.f('ix_users_phone'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('textile')
    op.drop_table('stores')
    op.drop_table('promotions')
    op.drop_table('categories')

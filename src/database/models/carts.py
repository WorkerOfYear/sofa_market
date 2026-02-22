import typing
import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.db import Base

if typing.TYPE_CHECKING:
    from src.database.models import Product, User


class Cart(Base):
    """Модель корзины."""

    __tablename__ = "carts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
        index=True,
    )
    session_id: Mapped[str | None] = mapped_column(
        String(64), nullable=True, index=True
    )
    total_price: Mapped[int] = mapped_column(default=0)
    is_deleted: Mapped[bool] = mapped_column(default=False)
    deleted_at: Mapped[datetime | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    user: Mapped["User"] = relationship(
        "User",
        back_populates="cart",
        single_parent=True,
        lazy="raise",
    )
    carts_products: Mapped[list["CartProduct"]] = relationship(
        "CartProduct",
        back_populates="cart",
        lazy="raise",
    )


class CartProduct(Base):
    """Модель продукта в корзине"""

    __tablename__ = "carts_products"

    id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(default=1)

    cart: Mapped["Cart"] = relationship(
        "Cart",
        back_populates="carts_products",
        single_parent=True,
        lazy="raise",
    )
    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="carts_products",
        single_parent=True,
        lazy="raise",
    )

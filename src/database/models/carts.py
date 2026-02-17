import typing

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.db import Base

if typing.TYPE_CHECKING:
    from src.database.models import Product, User


class Cart(Base):
    """Модель корзины."""

    __tablename__ = "carts"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    total_price: Mapped[int]

    user: Mapped["User"] = relationship(
        "User",
        back_populates="cart",
        single_parent=True,
        lazy="raise"
    )
    carts_products: Mapped[list["CartProduct"]] = relationship(
        "CartProduct",
        back_populates="cart",
        lazy="raise"
    )


class CartProduct(Base):
    """Модель продукта в корзине"""

    __tablename__ = "carts_products"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    cart_id: Mapped[int] = mapped_column(
        ForeignKey("carts.id")
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id")
    )

    quantity: Mapped[int]

    cart: Mapped["Cart"] = relationship(
        "Cart",
        back_populates="carts_products",
        single_parent=True,
        lazy="raise"
    )
    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="carts_products",
        single_parent=True,
        lazy="raise",
    )

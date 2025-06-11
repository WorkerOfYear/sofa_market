import typing

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.db import Base

if typing.TYPE_CHECKING:
    from src.database.models import Product, User


class Favorite(Base):
    """Модель желаемого."""

    __tablename__ = "favorites"

    id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), primary_key=True
    )
    user: Mapped["User"] = relationship(
        back_populates="favorite", single_parent=True
    )
    favorites_products: Mapped[list["FavoriteProduct"]] = relationship(
        "FavoriteProduct", back_populates="favorite"
    )


class FavoriteProduct(Base):
    """Модель продукта в желаемом"""

    __tablename__ = "favorites_products"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    favorite_id: Mapped[int] = mapped_column(
        ForeignKey("favorites.id")
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id")
    )
    favorite: Mapped["Favorite"] = relationship(
        "Favorite", back_populates="favorites_products", single_parent=True
    )
    product: Mapped["Product"] = relationship(
        "Product", back_populates="favorites_products", single_parent=True
    )

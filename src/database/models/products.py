import typing
from datetime import datetime

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.db import Base

if typing.TYPE_CHECKING:
    from src.database.models import (
        CartProduct,
        Category,
        FavoriteProduct,
        PurchaseProduct,
    )


class Product(Base):
    """Модель продукта."""

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    name: Mapped[str] = mapped_column(
        String(length=256)
    )
    slug: Mapped[str] = mapped_column(
        String(length=256)
    )
    description: Mapped[str] = mapped_column(
        String(length=256)
    )

    price: Mapped[int]

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id")
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), server_onupdate=func.now()
    )
    category: Mapped["Category"] = relationship(
        "Category",
        back_populates="products",
        single_parent=True,
        lazy="raise"
    )
    images: Mapped[list["Image"]] = relationship(
        "Image",
        back_populates="product",
        lazy="raise"
    )
    dimensions: Mapped[list["Dimension"]] = relationship(
        "Dimension",
        back_populates="product",
        lazy="raise"
    )
    carts_products: Mapped[list["CartProduct"]] = relationship(
        "CartProduct",
        back_populates="product",
        lazy="raise"
    )
    favorites_products: Mapped[list["FavoriteProduct"]] = relationship(
        "FavoriteProduct",
        back_populates="product",
        lazy="raise"
    )
    purchases_products: Mapped[list["PurchaseProduct"]] = relationship(
        "PurchaseProduct",
        back_populates="product",
        lazy="raise"
    )

    def __str__(self):
        return f"Товар:id - {self.id}, название - {self.name}"


class Image(Base):
    """Модель изображения."""

    __tablename__ = "images"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    url: Mapped[str]

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id")
    )
    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="images",
        single_parent=True,
        lazy="raise"
    )

    def __str__(self):
        return f"Изображение:id - {self.id}, продукт:id - {self.product_id}"


class Dimension(Base):
    """Модель размера."""

    __tablename__ = "dimensions"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    height: Mapped[str] = mapped_column(
        String(length=10)
    )
    width: Mapped[str] = mapped_column(
        String(length=10)
    )
    depth: Mapped[str] = mapped_column(
        String(length=10)
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id")
    )
    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="dimensions",
        single_parent=True,
        lazy="raise"
    )

    def __str__(self):
        return f"Размеры:id - {self.id}, продукт:id - {self.product_id}"

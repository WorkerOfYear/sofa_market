import typing
import uuid
from datetime import datetime

from sqlalchemy import Boolean, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.db import Base

if typing.TYPE_CHECKING:
    from src.database.models import Product, User


class Favorite(Base):
    """Модель желаемого."""

    __tablename__ = "favorites"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True
    )
    session_id: Mapped[str | None] = mapped_column(
        String(length=64), nullable=True, index=True
    )
    is_deleted: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    deleted_at: Mapped[datetime | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    user: Mapped["User"] = relationship(
        back_populates="favorites",
        single_parent=True,
        lazy="raise"
    )
    favorites_products: Mapped[list["FavoriteProduct"]] = relationship(
        "FavoriteProduct",
        back_populates="favorite",
        lazy="raise"
    )


class FavoriteProduct(Base):
    """Модель продукта в желаемом"""

    __tablename__ = "favorites_products"
    __table_args__ = (
        UniqueConstraint("favorite_id", "product_id", name="uq_favorite_product"),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    favorite_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("favorites.id")
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id")
    )
    favorite: Mapped["Favorite"] = relationship(
        "Favorite",
        back_populates="favorites_products",
        single_parent=True
    )
    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="favorites_products",
        single_parent=True
    )

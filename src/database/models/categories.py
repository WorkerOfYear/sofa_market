import typing
from datetime import date

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.db import Base

if typing.TYPE_CHECKING:
    from src.database.models import Product


class Category(Base):
    """Модель категории."""

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    name: Mapped[str] = mapped_column(
        String(length=256)
    )
    name_ru: Mapped[str | None] = mapped_column(
        String(length=256), nullable=True
    )
    name_kk: Mapped[str | None] = mapped_column(
        String(length=256), nullable=True
    )
    slug: Mapped[str] = mapped_column(
        String(length=256)
    )
    created_at: Mapped[date] = mapped_column(
        server_default=func.now()
    )
    products: Mapped[list["Product"]] = relationship(
        "Product",
        back_populates="category",
        lazy="raise"
    )

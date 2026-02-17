import typing
from datetime import datetime

from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.db import Base

if typing.TYPE_CHECKING:
    from src.database.models import Product


class Promotion(Base):
    """Модель акции/промоакции."""

    __tablename__ = "promotions"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    name: Mapped[str] = mapped_column(
        String(length=256)
    )
    discount_percent: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    valid_from: Mapped[datetime | None] = mapped_column(
        nullable=True
    )
    valid_until: Mapped[datetime | None] = mapped_column(
        nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), server_onupdate=func.now()
    )

    promotions_products: Mapped[list["PromotionProduct"]] = relationship(
        "PromotionProduct",
        back_populates="promotion",
        lazy="raise",
    )

    def __str__(self):
        return f"Promotion: {self.name} ({self.discount_percent}%)"


class PromotionProduct(Base):
    """Связь промоакции с продуктами."""

    __tablename__ = "promotions_products"
    __table_args__ = (
        UniqueConstraint("promotion_id", "product_id", name="uq_promotion_product"),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    promotion_id: Mapped[int] = mapped_column(
        ForeignKey("promotions.id")
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id")
    )

    promotion: Mapped["Promotion"] = relationship(
        "Promotion",
        back_populates="promotions_products",
        single_parent=True,
    )
    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="promotions_products",
        single_parent=True,
    )

    def __str__(self):
        return f"PromotionProduct: promotion_id={self.promotion_id}, product_id={self.product_id}"

import typing
from datetime import datetime
import uuid

from sqlalchemy import Enum, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.db import Base
from src.helpers.enums import PurchaseStatusEnum

if typing.TYPE_CHECKING:
    from src.database.models import Product, User


class Purchase(Base):
    """Модель покупки."""

    __tablename__ = "purchases"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    status: Mapped["PurchaseStatusEnum"] = mapped_column(
        Enum(PurchaseStatusEnum), nullable=False
    )
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now()
    )
    is_user_deleted: Mapped[bool] = mapped_column(
        default=False
    )
    user_deleted_at: Mapped[datetime | None] = mapped_column(
        nullable=True
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="purchases",
        single_parent=True,
        lazy="raise"
    )
    purchases_products: Mapped[list["PurchaseProduct"]] = relationship(
        "PurchaseProduct",
        back_populates="purchase",
        lazy="raise"
    )


class PurchaseProduct(Base):
    """Модель продукта в покупке."""

    __tablename__ = "purchases_products"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    purchase_id: Mapped[int] = mapped_column(
        ForeignKey("purchases.id")
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id")
    )
    quantity: Mapped[int]

    purchase: Mapped["Purchase"] = relationship(
        "Purchase",
        back_populates="purchases_products",
        single_parent=True
    )
    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="purchases_products",
        single_parent=True
    )

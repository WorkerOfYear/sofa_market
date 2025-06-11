from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.db import Base


class Store(Base):
    """Модель магазина."""

    __tablename__ = "stores"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    city: Mapped[str] = mapped_column(
        String(length=100)
    )
    address: Mapped[str] = mapped_column(
        String(length=100)
    )
    description: Mapped[str] = mapped_column(
        String(length=400)
    )

    def __str__(self):
        return f"Магазин:id - {self.id}, аддрес - {self.address}"

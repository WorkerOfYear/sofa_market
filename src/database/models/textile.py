from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.db import Base


class Textile(Base):
    """Модель ткани."""

    __tablename__ = "textile"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    producer: Mapped[str] = mapped_column(
        String(length=256)
    )
    color: Mapped[str] = mapped_column(
        String(length=256)
    )
    description: Mapped[str] = mapped_column(
        String(length=512)
    )
    is_available: Mapped[bool] = mapped_column(
        default=True
    )

    def __str__(self):
        return (
            f"Ткань:id - {self.id}, "
            f"цвет - {self.color}, "
            f"производитель - {self.producer}"
        )

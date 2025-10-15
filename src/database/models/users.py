from datetime import datetime
from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.db import Base

if TYPE_CHECKING:
    from src.database.models import Cart, Favorite, Purchase


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"

    # Обязательные поля уже есть в SQLAlchemyBaseUserTableUUID:
    # id: UUID, email: str, hashed_password: str, is_active: bool, etc.

    first_name: Mapped[str | None] = mapped_column(String(length=100))
    last_name: Mapped[str | None] = mapped_column(String(length=150))
    phone: Mapped[str] = mapped_column(String(length=20), unique=True, nullable=False)
    city: Mapped[str] = mapped_column(String(length=100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    cart: Mapped["Cart"] = relationship(
        "Cart", back_populates="user", cascade="all, delete-orphan"
    )
    favorite: Mapped["Favorite"] = relationship(
        "Favorite", back_populates="user", cascade="all, delete-orphan"
    )
    purchases: Mapped[list["Purchase"]] = relationship(
        "Purchase", back_populates="user", cascade="all, delete-orphan"
    )

    def __str__(self):
        return f"Пользователь: {self.phone}"

    def to_read_model(self):
        from src.schemas.users import UserReadSchema
        return UserReadSchema.model_validate(self)
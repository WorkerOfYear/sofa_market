import typing
from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression

from src.database.db import Base
from src.schemas.users import UserReadSchema

if typing.TYPE_CHECKING:
    from src.database.models import Cart, Favorite, Purchase


class User(SQLAlchemyBaseUserTable[int], Base):
    """Модель пользователя."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    first_name: Mapped[str | None] = mapped_column(
        String(length=100)
    )
    last_name: Mapped[str | None] = mapped_column(
        String(length=150)
    )
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True
    )
    phone: Mapped[str] = mapped_column(
        String(length=100), unique=True, nullable=False
    )
    city: Mapped[str] = mapped_column(
        String(length=100), nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        server_default=expression.true()
    )
    is_superuser: Mapped[bool] = mapped_column(
        server_default=expression.false()
    )
    is_verified: Mapped[bool] = mapped_column(
        server_default=expression.false()
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), server_onupdate=func.now()
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
        return f"Пользователь:id - {self.id}, phone - {self.phone}"

    def to_read_model(self):
        return UserReadSchema.model_validate(self)

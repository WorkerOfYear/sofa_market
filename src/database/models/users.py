import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, func, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from src.database.db import Base
from src.schemas.users import UserBase

if TYPE_CHECKING:
    from src.database.models import Cart, Favorite, Purchase


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str | None] = mapped_column(
        String(length=320), nullable=True, index=True
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    first_name: Mapped[str | None] = mapped_column(
        String(length=256), nullable=True
    )
    last_name: Mapped[str | None] = mapped_column(
        String(length=256), nullable=True
    )
    phone: Mapped[str] = mapped_column(
        String(length=20), unique=True, index=True
    )
    city: Mapped[str | None] = mapped_column(
        String(length=128), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    cart: Mapped["Cart"] = relationship(
        "Cart",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="raise_on_sql"
    )
    favorite: Mapped["Favorite"] = relationship(
        "Favorite",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="raise_on_sql"
    )
    purchases: Mapped[list["Purchase"]] = relationship(
        "Purchase",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="raise_on_sql"
    )

    def __str__(self):
        return f"Пользователь: {self.email}"

    def to_base_scheme(self) -> UserBase:
        return UserBase.model_validate(self)

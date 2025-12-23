from typing import Sequence

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import UserBase
from src.database.models import User

from .base import SQLAlchemyRepository


class UsersRepository(SQLAlchemyRepository[User]):
    model = User

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create(self, data: UserBase) -> User:
        user = User(**data.model_dump())
        self._session.add(user)
        await self._session.flush()
        return user

    async def get_all(self) -> Sequence[User]:
        stmt = select(self.model)
        result = await self._session.scalars(stmt) # Посмотреть различия scalars и execute
        return result.all()

    async def get_by_id(self, id_: int) -> User | None:
        stmt = select(self.model).where(self.model.id == id_)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(self.model).where(self.model.email == email)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_phone(self, phone: str) -> User | None:
        stmt = select(self.model).where(self.model.phone == phone)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def activate_user(self, user_id: int) -> None:
        stmt = (
            update(self.model)
            .where(self.model.id == user_id)
            .values(is_active=True)
            .returning(self.model)
        )
        await self._session.execute(stmt)

    async def deactivate_user(self, user_id: int) -> None:
        stmt = (
            update(self.model)
            .where(self.model.id == user_id)
            .values(is_active=False)
            .returning(self.model)
        )
        await self._session.execute(stmt)

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User

from .base import SQLAlchemyRepository


class UsersRepository(SQLAlchemyRepository[User]):
    model = User

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def add(self, data: dict) -> User:
        user = User(**data)
        self._session.add(user)
        await self._session.flush()
        return user

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(self.model).where(self.model.email == email)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_phone(self, phone: str) -> User | None:
        stmt = select(self.model).where(self.model.phone == phone)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def find_by_credentials(self, email: str, password: str) -> User | None:
        stmt = select(self.model).where(self.model.email == email, self.model.hashed_password == password)
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

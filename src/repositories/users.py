from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User

from .base import SQLAlchemyRepository


class UsersRepository(SQLAlchemyRepository[User]):
    model = User

    async def get_by_email(self, email: str, session: AsyncSession | None = None) -> User | None:
        stmt = select(self.model).where(self.model.email == email)
        result = await self._execute_in_transaction(stmt, session)
        return result.scalar_one_or_none()

    async def get_by_phone(self, phone: str, session: AsyncSession | None = None) -> User | None:
        stmt = select(self.model).where(self.model.phone == phone)
        result = await self._execute_in_transaction(stmt, session)
        return result.scalar_one_or_none()

    async def find_by_credentials(self, email: str, password: str, session: AsyncSession | None = None) -> User | None:
        stmt = select(self.model).where(self.model.email == email, self.model.hash_password == password)
        result = await self._execute_in_transaction(stmt, session)
        return result.scalar_one_or_none()

    async def activate_user(self, user_id: int, session: AsyncSession | None = None) -> None:
        stmt = (
            update(self.model)
            .where(self.model.id == user_id)
            .values(is_active=True)
            .returning(self.model)
        )
        result = await self._execute_in_transaction(stmt, session)
        return result.scalar_one_or_none()

    async def deactivate_user(self, user_id: int, session: AsyncSession | None = None) -> None:
        stmt = (
            update(self.model)
            .where(self.model.id == user_id)
            .values(is_active=False)
            .returning(self.model)
        )
        result = await self._execute_in_transaction(stmt, session)
        return result.scalar_one_or_none()

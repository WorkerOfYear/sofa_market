from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Any, Type, Sequence
from uuid import UUID

from sqlalchemy import insert, select, update, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select, Delete, Update, Insert

from src.database.connection import async_session_maker
from src.database.db import Base


M = TypeVar('M', bound=Base)
ID = TypeVar('ID', int, UUID, str)


class AbstractRepository(ABC, Generic[M]):
    @abstractmethod
    async def add_one(self, data: dict[str, Any], session: AsyncSession | None = None) -> M:
        raise NotImplementedError

    @abstractmethod
    async def add_many(self, data: list[dict[str, Any]], session: AsyncSession | None = None) -> Sequence[M]:
        raise NotImplementedError

    @abstractmethod
    async def find_all(self, session: AsyncSession | None = None) -> Sequence[M]:
        raise NotImplementedError

    @abstractmethod
    async def find_by_id(self, id_: ID, session: AsyncSession | None = None) -> M | None:
        raise NotImplementedError

    @abstractmethod
    async def find_by_query(self, query: dict[str, Any], session: AsyncSession | None = None) -> Sequence[M]:
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, id_: ID, data: dict[str, Any], session: AsyncSession | None = None) -> M | None:
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, id_: ID, session: AsyncSession | None = None) -> M | None:
        raise NotImplementedError

    @abstractmethod
    async def delete_all(self, session: AsyncSession | None = None) -> None:
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository[M]):
    model: Type[M]

    @staticmethod
    async def _execute_in_transaction(
            stmt: Select | Update | Delete | Insert,
            session: AsyncSession | None = None
    ) -> Any:
        if session:
            result = await session.execute(stmt)
            return result
        async with async_session_maker() as new_session:
            result = await new_session.execute(stmt)
            await new_session.commit()
            return result

    async def add_one(
            self,
            data: dict[str, Any],
            session: AsyncSession | None = None
    ) -> M:
        stmt = insert(self.model).values(**data).returning(self.model)
        result = await self._execute_in_transaction(stmt, session)
        return result.scalar_one()

    async def add_many(
            self,
            data: list[dict[str, Any]],
            session: AsyncSession | None = None
    ) -> Sequence[M]:
        stmt = insert(self.model).returning(self.model)
        result = await self._execute_in_transaction(stmt.values(data), session)
        return result.scalars().all()

    async def find_all(
            self,
            session: AsyncSession | None = None
    ) -> Sequence[M]:
        stmt = select(self.model)
        result = await self._execute_in_transaction(stmt, session)
        return result.scalars().all()

    async def find_by_id(
            self,
            id_: ID,
            session: AsyncSession | None = None
    ) -> M | None:
        stmt = select(self.model).where(self.model.id == id_)
        result = await self._execute_in_transaction(stmt, session)
        return result.scalar_one_or_none()

    async def find_by_query(
            self,
            query: dict[str, Any],
            session: AsyncSession | None = None
    ) -> Sequence[M]:
        stmt = select(self.model)
        conditions = []
        for field, value in query.items():
            if hasattr(self.model, field):
                conditions.append(getattr(self.model, field) == value)
        if conditions:
            stmt = stmt.where(and_(*conditions))
        result = await self._execute_in_transaction(stmt, session)
        return result.scalars().all()

    async def update_one(
            self,
            id_: ID,
            data: dict[str, Any],
            session: AsyncSession | None = None
    ) -> M | None:
        stmt = (
            update(self.model)
            .where(self.model.id == id_)
            .values(**data)
            .returning(self.model)
        )
        result = await self._execute_in_transaction(stmt, session)
        return result.scalar_one_or_none()

    async def delete_one(
            self,
            id_: ID,
            session: AsyncSession | None = None
    ) -> M | None:
        stmt = (
            delete(self.model)
            .where(self.model.id == id_)
            .returning(self.model)
        )
        result = await self._execute_in_transaction(stmt, session)
        return result.scalar_one_or_none()

    async def delete_all(
            self,
            session: AsyncSession | None = None
    ) -> None:
        stmt = delete(self.model)
        await self._execute_in_transaction(stmt, session)

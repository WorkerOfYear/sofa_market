from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type
from uuid import UUID

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import Base


M = TypeVar('M', bound=Base)
ID = TypeVar('ID', int, UUID, str)


class AbstractRepository(ABC, Generic[M]):
    @abstractmethod
    async def _find_by_id(self, id_: ID) -> M | None:
        raise NotImplementedError

    @abstractmethod
    async def _update(self, id_: ID, **values) -> None:
        raise NotImplementedError

    @abstractmethod
    async def _delete(self, id_: ID) -> None:
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository[M]):
    model: Type[M]

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def _find_by_id(self, id_: ID) -> M | None:
        stmt = select(self.model).where(self.model.id == id_)
        res = await self._session.execute(stmt)
        return res.scalar_one_or_none()

    async def _update(self, id_: ID, **values) -> None:
        stmt = update(self.model).where(self.model.id == id_).values(**values)
        await self._session.execute(stmt)

    async def _delete(self, id_: ID) -> None:
        stmt = delete(self.model).where(self.model.id == id_)
        await self._session.execute(stmt)

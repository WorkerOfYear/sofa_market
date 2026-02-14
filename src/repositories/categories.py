from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Category

from .base import SQLAlchemyRepository


class CategoriesRepository(SQLAlchemyRepository[Category]):
    model = Category

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def get_all(self) -> Sequence[Category]:
        stmt = select(self.model).order_by(self.model.name)
        result = await self._session.scalars(stmt)
        return result.all()

    async def get_by_slug(self, slug: str) -> Category | None:
        stmt = select(self.model).where(self.model.slug == slug)
        result = await self._session.scalars(stmt)
        return result.first()

    async def get_by_id(self, id_: int) -> Category | None:
        stmt = select(self.model).where(self.model.id == id_)
        result = await self._session.scalars(stmt)
        return result.first()

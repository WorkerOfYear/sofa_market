from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Product

from .base import SQLAlchemyRepository


class ProductsRepository(SQLAlchemyRepository[Product]):
    model = Product

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_all(self) -> Sequence[Product]:
        stmt = select(self.model).options(
            selectinload(self.model.images),
            selectinload(self.model.dimensions),
        )
        result = await self._session.scalars(stmt)
        return result.all()

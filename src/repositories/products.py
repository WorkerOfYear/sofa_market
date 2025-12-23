from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Product

from .base import SQLAlchemyRepository
from ..schemas import ProductCreate


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

    async def create(self, data: ProductCreate) -> Product:
        db_obj = self.model(**data.model_dump())
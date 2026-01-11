from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src import schemas
from src.database.models import Product, Dimension, Image

from .base import SQLAlchemyRepository


class ProductsRepository(SQLAlchemyRepository[Product]):
    model = Product

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_products(self) -> Sequence[Product]:
        stmt = select(self.model).options(
            selectinload(self.model.images),
            selectinload(self.model.dimensions),
        )
        result = await self._session.scalars(stmt)
        return result.all()

    async def get_product(self, product_id: int) -> Product | None:
        stmt = select(self.model).filter(
            self.model.id == product_id,
        ).options(
            selectinload(self.model.images),
            selectinload(self.model.dimensions),
        )
        result = await self._session.scalars(stmt)
        return result.first()

    async def create_product(self, data: schemas.ProductCreate) -> Product:
        product = self.model(**data.model_dump())
        self._session.add(product)
        await self._session.flush()
        await self._session.refresh(product)
        return product

    async def create_dimension(self, data: schemas.DimensionCreate) -> Dimension:
        dimension = Dimension(**data.model_dump())
        self._session.add(dimension)
        await self._session.flush()
        return dimension

    async def create_image(self, data: schemas.ImageCreate) -> Image:
        image = Image(**data.model_dump())
        self._session.add(image)
        await self._session.flush()
        return image

from typing import Sequence

from sqlalchemy import select, func, or_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src import schemas
from src.database.models import Product, Dimension, Image, Category

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

        result = await self._session.execute(
            select(self.model)
            .options(
                selectinload(self.model.images),
                selectinload(self.model.dimensions),
            )
            .where(self.model.id == product.id)
        )
        product = result.scalar_one()
        return product

    async def delete_product(self, product_id: int) -> None:
        return await self._delete(product_id)

    async def create_dimension(self, data: schemas.DimensionCreate) -> Dimension:
        dimension = Dimension(**data.model_dump())
        self._session.add(dimension)
        await self._session.flush()
        return dimension

    async def delete_dimension(self, dimension_id: int) -> None:
        stmt = select(Dimension).filter(Dimension.id == dimension_id)
        result = await self._session.scalars(stmt)
        dimension = result.first()
        if dimension:
            await self._session.delete(dimension)

    async def get_image(self, image_id: int) -> Image | None:
        stmt = select(Image).filter(Image.id == image_id)
        result = await self._session.scalars(stmt)
        return result.first()

    async def create_image(self, data: schemas.ImageCreate) -> Image:
        image = Image(
            product_id=data.product_id,
            storage_type=data.storage_type,
            url=data.url
        )
        self._session.add(image)
        await self._session.flush()
        return image

    async def delete_image(self, image_id: int) -> None:
        stmt = select(Image).filter(Image.id == image_id)
        result = await self._session.scalars(stmt)
        image = result.first()
        if image:
            await self._session.delete(image)

    async def search_products(
        self,
        category_slug: str | None = None,
        query: str | None = None,
        min_price: int | None = None,
        max_price: int | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[Sequence[Product], int]:
        stmt = (
            select(Product)
            .join(Category, Product.category_id == Category.id)
            .options(
                selectinload(Product.images),
                selectinload(Product.dimensions),
            )
        )
        count_stmt = select(func.count()).select_from(Product).join(
            Category, Product.category_id == Category.id
        )

        if category_slug is not None:
            stmt = stmt.where(Category.slug == category_slug)
            count_stmt = count_stmt.where(Category.slug == category_slug)

        if query:
            pattern = f"%{query}%"
            stmt = stmt.where(
                or_(
                    Product.name.ilike(pattern),
                    Product.description.ilike(pattern),
                )
            )
            count_stmt = count_stmt.where(
                or_(
                    Product.name.ilike(pattern),
                    Product.description.ilike(pattern),
                )
            )

        if min_price is not None:
            stmt = stmt.where(Product.price >= min_price)
            count_stmt = count_stmt.where(Product.price >= min_price)

        if max_price is not None:
            stmt = stmt.where(Product.price <= max_price)
            count_stmt = count_stmt.where(Product.price <= max_price)

        total = await self._session.scalar(count_stmt) or 0

        stmt = stmt.order_by(Product.created_at.desc()).limit(limit).offset(
            offset
        )
        result = await self._session.scalars(stmt)
        products = result.all()

        return products, total

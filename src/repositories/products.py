from datetime import datetime
from typing import Sequence

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src import schemas
from src.database.models import (
    Category,
    Dimension,
    Image,
    Product,
    Promotion,
    PromotionProduct,
)

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
        stmt = (
            select(self.model)
            .filter(
                self.model.id == product_id,
            )
            .options(
                selectinload(self.model.images),
                selectinload(self.model.dimensions),
            )
        )
        result = await self._session.scalars(stmt)
        return result.first()

    async def get_discounts_for_products(
        self, product_ids: list[int]
    ) -> dict[int, int]:
        """
        Get best active discount for each product.
        Returns {product_id: discount_percent}.
        """
        if not product_ids:
            return {}

        now = datetime.now()

        stmt = (
            select(
                PromotionProduct.product_id,
                func.max(Promotion.discount_percent).label("discount"),
            )
            .join(Promotion, PromotionProduct.promotion_id == Promotion.id)
            .where(
                PromotionProduct.product_id.in_(product_ids),
                or_(
                    Promotion.valid_until.is_(None),
                    Promotion.valid_until > now,
                ),
                or_(
                    Promotion.valid_from.is_(None), Promotion.valid_from <= now
                ),
            )
            .group_by(PromotionProduct.product_id)
        )

        result = await self._session.execute(stmt)
        return {row.product_id: row.discount for row in result}

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
        filters: schemas.ProductCatalogFilters,
        category_slug: str | None = None,
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

        if filters.query:
            pattern = f"%{filters.query}%"
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

        if filters.min_price is not None:
            stmt = stmt.where(Product.price >= filters.min_price)
            count_stmt = count_stmt.where(Product.price >= filters.min_price)

        if filters.max_price is not None:
            stmt = stmt.where(Product.price <= filters.max_price)
            count_stmt = count_stmt.where(Product.price <= filters.max_price)

        total = await self._session.scalar(count_stmt) or 0

        stmt = stmt.order_by(Product.created_at.desc()).limit(
            filters.limit
        ).offset(filters.offset)

        result = await self._session.scalars(stmt)
        products = result.all()

        return products, total

from fastapi import HTTPException

from src import schemas
from src.uow.sqlalchemy import UnitOfWork
from src.database.models import Product


class CatalogService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_categories(self) -> list:
        return list(await self.uow.category_repo.get_all())

    async def get_products_by_category(
        self,
        category_slug: str,
        query: str | None = None,
        min_price: int | None = None,
        max_price: int | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[Product], int]:
        category = await self.uow.category_repo.get_by_slug(category_slug)
        if not category:
            raise HTTPException(
                status_code=404,
                detail="Category not found",
            )
        return await self.uow.product_repo.search_products(
            category_slug=category_slug,
            query=query,
            min_price=min_price,
            max_price=max_price,
            limit=limit,
            offset=offset,
        )

    async def get_product(self, product_id: int) -> Product:
        product = await self.uow.product_repo.get_product(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

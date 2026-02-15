from fastapi import HTTPException

from src import schemas
from src.uow.sqlalchemy import UnitOfWork
from src.database.models import Product, Category
from src.helpers.translation import localized


class CatalogService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_categories(self) -> list:
        return list(await self.uow.category_repo.get_all())

    async def get_products_by_category(
            self, filters: schemas.ProductCatalogFilters, category_slug: str
    ) -> tuple[list[Product], int]:

        category = await self.uow.category_repo.get_by_slug(category_slug)
        if not category:
            raise HTTPException(
                status_code=404,
                detail="Category not found",
            )
        return await self.uow.product_repo.search_products(
            filters, category_slug=category_slug
        )

    async def get_product(self, product_id: int) -> Product:
        product = await self.uow.product_repo.get_product(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

    @staticmethod
    def map_category(category: Category, locale: str) -> schemas.CategoryCatalogItem:
        return schemas.CategoryCatalogItem.model_validate({
            "id": category.id,
            "name": localized(category, "name", locale),
            "slug": category.slug,
            "created_at": category.created_at,
        })

    @staticmethod
    def map_product(product: Product, locale: str) -> schemas.ProductCatalogItem:
        return schemas.ProductCatalogItem.model_validate({
            "id": product.id,
            "name": localized(product, "name", locale),
            "slug": product.slug,
            "description": localized(product, "description", locale),
            "price": product.price,
            "category_id": product.category_id,
            "created_at": product.created_at,
            "updated_at": product.updated_at,
            "images": product.images,
            "dimensions": product.dimensions,
        })

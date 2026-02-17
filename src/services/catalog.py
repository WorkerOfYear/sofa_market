from fastapi import HTTPException

from src import schemas
from src.database.models import Category, Product
from src.helpers.promotions import calculate_current_price
from src.helpers.translation import localized
from src.uow.sqlalchemy import UnitOfWork


class CatalogService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_categories(self) -> list[Category]:
        return list(await self.uow.category_repo.get_all())

    def map_category(
        self, category: Category, locale: str
    ) -> schemas.CategoryCatalogItem:
        return schemas.CategoryCatalogItem(
            id=category.id,
            name=localized(category, "name", locale),
            slug=category.slug,
            created_at=category.created_at,
        )

    async def map_product(
        self, product: Product, locale: str, discount_percent: int = 0
    ) -> schemas.ProductCatalogItem:
        return schemas.ProductCatalogItem(
            id=product.id,
            name=localized(product, "name", locale),
            slug=product.slug,
            description=localized(product, "description", locale),
            price=product.price,
            current_price=calculate_current_price(
                product.price, discount_percent
            ),
            is_on_promotion=discount_percent > 0,
            discount_percent=discount_percent,
            category_id=product.category_id,
            created_at=product.created_at,
            updated_at=product.updated_at,
            images=product.images,
            dimensions=product.dimensions,
        )

    async def get_products_by_category(
        self,
        filters: schemas.ProductCatalogFilters,
        category_slug: str,
        locale: str = "ru",
    ) -> tuple[list[schemas.ProductCatalogItem], int]:
        category = await self.uow.category_repo.get_by_slug(category_slug)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        products, total = await self.uow.product_repo.search_products(
            filters, category_slug=category_slug
        )

        # Batch fetch discounts for all products
        product_ids = [p.id for p in products]
        discounts = await self.uow.product_repo.get_discounts_for_products(
            product_ids
        )

        # Map products with their discounts
        items = [
            await self.map_product(p, locale, discounts.get(p.id, 0))
            for p in products
        ]
        return items, total

    async def get_product(
        self, product_id: int, locale: str = "ru"
    ) -> schemas.ProductCatalogItem:
        product = await self.uow.product_repo.get_product(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        # Fetch discount for single product
        discounts = await self.uow.product_repo.get_discounts_for_products(
            [product.id]
        )
        discount = discounts.get(product.id, 0)

        return await self.map_product(product, locale, discount)

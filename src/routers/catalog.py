from fastapi import APIRouter, Depends

from src import schemas
from src.dependencies import get_catalog_service, get_locale
from src.schemas.catalog import ProductCatalogFilters
from src.services import CatalogService

router = APIRouter(tags=["catalog"])


@router.get("/categories", response_model=list[schemas.CategoryCatalogItem])
async def list_categories(
    catalog_service: CatalogService = Depends(get_catalog_service),
    locale: str = Depends(get_locale),
):
    """List all categories (public, no auth)."""
    categories = await catalog_service.get_categories()
    return [catalog_service.map_category(c, locale) for c in categories]


@router.get("/categories/{category_slug}", response_model=schemas.ProductSearchResult)
async def get_products_by_category(
    category_slug: str,
    filters: ProductCatalogFilters = Depends(),
    catalog_service: CatalogService = Depends(get_catalog_service),
    locale: str = Depends(get_locale),
):
    """Products in category with optional filters (public, no auth)."""
    items, total = await catalog_service.get_products_by_category(
        filters, category_slug, locale
    )
    return schemas.ProductSearchResult(
        items=items,
        total=total,
        limit=filters.limit,
        offset=filters.offset,
    )


@router.get("/products/{product_id}", response_model=schemas.ProductCatalogItem)
async def get_product(
    product_id: int,
    catalog_service: CatalogService = Depends(get_catalog_service),
    locale: str = Depends(get_locale),
):
    """Product detail (public, no auth)."""
    return await catalog_service.get_product(product_id, locale)

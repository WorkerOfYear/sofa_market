from fastapi import APIRouter, Depends, Query

from src import schemas
from src.dependencies import get_catalog_service
from src.services import CatalogService

router = APIRouter(tags=["catalog"])


@router.get("/categories", response_model=list[schemas.CategoryBase])
async def list_categories(
    catalog_service: CatalogService = Depends(get_catalog_service),
):
    return await catalog_service.get_categories()


@router.get("/categories/{category_slug}")
async def get_products_by_category(
    category_slug: str,
    query: str | None = Query(None, description="Search in name/description"),
    min_price: int | None = Query(None, ge=0),
    max_price: int | None = Query(None, ge=0),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    catalog_service: CatalogService = Depends(get_catalog_service),
):
    products, total = await catalog_service.get_products_by_category(
        category_slug=category_slug,
        query=query,
        min_price=min_price,
        max_price=max_price,
        limit=limit,
        offset=offset,
    )
    return schemas.ProductSearchResult(
        items=[schemas.ProductBase.model_validate(p) for p in products],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/products/{product_id}", response_model=schemas.ProductBase)
async def get_product(
    product_id: int,
    catalog_service: CatalogService = Depends(get_catalog_service),
):
    return await catalog_service.get_product(product_id)

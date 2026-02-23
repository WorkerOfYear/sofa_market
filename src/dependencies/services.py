from fastapi import Depends

from src.dependencies import get_storage_client
from src.helpers.storage import StorageClient
from src.services import (
    CatalogService,
    FavoritesService,
    ImageService,
    ProductsService,
    PromotionsService,
    PurchasesService,
)
from src.services.carts import CartsService
from src.uow.sqlalchemy import UnitOfWork

from .uow import get_uow


async def get_images_service(
    storage: StorageClient = Depends(get_storage_client),
) -> ImageService:
    return ImageService(storage)


async def get_products_service(
    uow: UnitOfWork = Depends(get_uow),
) -> ProductsService:
    return ProductsService(uow)


async def get_catalog_service(
    uow: UnitOfWork = Depends(get_uow),
) -> CatalogService:
    return CatalogService(uow)


async def get_promotions_service(
    uow: UnitOfWork = Depends(get_uow),
) -> PromotionsService:
    return PromotionsService(uow)


async def get_carts_service(
    uow: UnitOfWork = Depends(get_uow),
) -> CartsService:
    return CartsService(uow)


async def get_favorites_service(
    uow: UnitOfWork = Depends(get_uow),
) -> FavoritesService:
    return FavoritesService(uow)


async def get_purchases_service(
    uow: UnitOfWork = Depends(get_uow),
) -> PurchasesService:
    return PurchasesService(uow)

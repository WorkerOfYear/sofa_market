from fastapi import Depends

from src.dependencies import get_uow, get_storage_client
from src.uow.sqlalchemy import UnitOfWork
from src.helpers.storage import StorageClient
from src.services import (
    ImageService,
    ProductsService,
    CatalogService,
)


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

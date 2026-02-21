from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, File

from src import schemas
from src.dependencies import (
    get_current_user,
    get_products_service,
    get_search_service,
    get_storage_client,
)
from src.helpers.enums import ImageStorageTypeEnum, StorageDirectory
from src.helpers.storage import LocalStorageClient
from src.search import SearchService
from src.search.documents import product_to_doc
from src.services import ProductsService

router = APIRouter(tags=["products"], dependencies=[Depends(get_current_user)])


@router.get("", response_model=list[schemas.ProductBase])
async def get_products(
        product_service: ProductsService = Depends(get_products_service)
):
    return await product_service.get_products()


@router.get("/{product_id}", response_model=schemas.ProductBase)
async def get_product(
        product_id: int,
        product_service: ProductsService = Depends(get_products_service),
):
    return await product_service.get_product(product_id)


@router.post("", response_model=schemas.ProductBase)
async def create_product(
        data: schemas.ProductCreate,
        product_service: ProductsService = Depends(get_products_service),
        search_service: SearchService = Depends(get_search_service),
):
    product = await product_service.create_product(data)
    category = await product_service.uow.category_repo.get_by_id(product.category_id)
    await search_service.index_product(product_to_doc(product, category))
    return product


@router.delete("/{product_id}")
async def delete_product(
        product_id: int,
        product_service: ProductsService = Depends(get_products_service),
        search_service: SearchService = Depends(get_search_service),
):
    await product_service.delete_product(product_id)
    await search_service.delete_product(product_id)


@router.post("/dimension", response_model=schemas.DimensionBase)
async def create_dimension(
        data: schemas.DimensionCreate,
        product_service: ProductsService = Depends(get_products_service),
):
    return await product_service.create_dimension(data)


@router.delete("/dimension/{dimension_id}")
async def delete_dimension(
        dimension_id: int,
        product_service: ProductsService = Depends(get_products_service),
):
    return await product_service.delete_dimension(dimension_id)


@router.get("/image/{image_id}", response_model=bytes)
async def get_image(
        image_id: int,
        product_service: ProductsService = Depends(get_products_service),
        storage_client: LocalStorageClient = Depends(get_storage_client),
):
    db_image = await product_service.get_image(image_id)
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")

    image = await storage_client.read_file(str(db_image.url), StorageDirectory.PRODUCTS)
    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return image


@router.post("/image/{product_id}", response_model=schemas.ImageBase)
async def create_image(
        product_id: int,
        storage_type: ImageStorageTypeEnum,
        image: Annotated[bytes, File()],
        product_service: ProductsService = Depends(get_products_service),
        storage_client: LocalStorageClient = Depends(get_storage_client),
):
    product = await product_service.get_product(product_id)

    if storage_type == ImageStorageTypeEnum.LOCAL:
        filename = f"image-{len(product.images) + 1}.jpg"
        file_path = Path(storage_client.products_dir) / filename
        await storage_client.upload_file(file_bytes=image, destination=file_path)
    else:
        raise HTTPException(status_code=404, detail="Storage type not supported")

    image_db = await product_service.create_image(schemas.ImageCreate(
        product_id=product_id,
        storage_type=ImageStorageTypeEnum.LOCAL,
        url=str(filename)
    ))
    return image_db


@router.delete("/image/{image_id}")
async def delete_image(
        image_id: int,
        product_service: ProductsService = Depends(get_products_service),
        storage_client: LocalStorageClient = Depends(get_storage_client),
):
    db_image = await product_service.get_image(image_id)
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")

    await storage_client.delete_file(str(db_image.url), StorageDirectory.PRODUCTS)
    await product_service.delete_image(image_id)

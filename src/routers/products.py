from fastapi import APIRouter, Depends

from src import schemas
from src.services import ProductsService, ImageService
from src.dependencies import get_current_user, get_products_service, get_storage_client
from src.helpers.storage import StorageClient, LocalStorageClient

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
):
    return await product_service.create_product(data)


@router.post("/dimension", response_model=schemas.DimensionBase)
async def create_dimension():
    return


@router.patch("/dimension/{dimension_id}", response_model=schemas.DimensionBase)
async def update_dimension(dimension_id: int):
    return


@router.delete("/dimension/{dimension_id}")
async def delete_dimension(dimension_id: int):
    return


@router.get("/image/{image_id}", response_model=schemas.ImageBase)
async def get_image(image_id: int):
    return


@router.post("/image", response_model=schemas.ImageBase)
async def create_image(
        product_service: ProductsService = Depends(get_products_service),
        sotrage_client: StorageClient = Depends(get_storage_client),
):
    ...


@router.delete("/image/{image_id}")
async def delete_image(image_id: int):
    return

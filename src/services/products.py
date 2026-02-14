from fastapi import HTTPException

from src import schemas
from src.uow.sqlalchemy import UnitOfWork
from src.database.models import Product, Dimension, Image


class ProductsService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_products(self) -> list[Product]:
        return await self.uow.product_repo.get_products()

    async def get_product(self, product_id: int) -> Product:
        product = await self.uow.product_repo.get_product(product_id)
        if not product:
            raise HTTPException(status_code=404)
        return product

    async def is_product_exist(self, product_id: int) -> bool:
        if await self.uow.product_repo.get_product(product_id):
            return True
        return False

    async def create_product(self, data: schemas.ProductCreate) -> Product:
        return await self.uow.product_repo.create_product(data)

    async def delete_product(self, product_id: int) -> None:
        return await self.uow.product_repo.delete_product(product_id)

    async def create_dimension(self, data: schemas.DimensionCreate) -> Dimension:
        return await self.uow.product_repo.create_dimension(data)

    async def delete_dimension(self, dimension_id: int) -> None:
        return await self.uow.product_repo.delete_dimension(dimension_id)

    async def get_image(self, image_id: int) -> Image | None:
        return await self.uow.product_repo.get_image(image_id)

    async def create_image(self, data: schemas.ImageCreate) -> Image:
        return await self.uow.product_repo.create_image(data)

    async def delete_image(self, image_id: int) -> None:
        return await self.uow.product_repo.delete_image(image_id)

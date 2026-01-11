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

    async def create_product(self, data: schemas.ProductCreate) -> Product:
        return await self.uow.product_repo.create_product(data)

    async def create_dimension(self, data: schemas.DimensionCreate) -> Dimension:
        return await self.uow.product_repo.create_dimension(data)

    async def create_image(self, data: schemas.ImageCreate) -> Image:
        return await self.uow.product_repo.create_image(data)

from src.uow.sqlalchemy import UnitOfWork
from src.database.models import Product
from src.schemas import ProductCreate


class ProductsService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_all(self) -> list[Product]:
        return await self.uow.product_repo.get_all()

    async def create(self, data: ProductCreate) -> Product:
        self.uow.product_repo.create()
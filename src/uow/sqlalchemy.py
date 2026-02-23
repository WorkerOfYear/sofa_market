from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.repositories.carts import CartsRepository
from src.repositories.categories import CategoriesRepository
from src.repositories.favorites import FavoritesRepository
from src.repositories.products import ProductsRepository
from src.repositories.promotions import PromotionsRepository
from src.repositories.purchases import PurchasesRepository
from src.repositories.users import UsersRepository
from src.uow.base import AbstractUnitOfWork


class UnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self.session_factory = session_factory
        self.session: AsyncSession | None = None

    @asynccontextmanager
    async def __call__(self):
        self.session: AsyncSession = self.session_factory()
        try:
            self.user_repo = UsersRepository(self.session)
            self.product_repo = ProductsRepository(self.session)
            self.category_repo = CategoriesRepository(self.session)
            self.promotion_repo = PromotionsRepository(self.session)
            self.cart_repo = CartsRepository(self.session)
            self.favorite_repo = FavoritesRepository(self.session)
            self.purchase_repo = PurchasesRepository(self.session)

            yield self
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise
        finally:
            await self.session.close()

    async def commit(self):
        if self.session is not None:
            await self.session.commit()

    async def rollback(self):
        if self.session is not None:
            await self.session.rollback()

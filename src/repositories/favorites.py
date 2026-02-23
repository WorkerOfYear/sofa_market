import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database.models import Favorite, FavoriteProduct, Product

from .base import SQLAlchemyRepository


class FavoritesRepository(SQLAlchemyRepository[Favorite]):
    model = Favorite

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    def _active_query(self):
        return select(self.model).where(self.model.is_deleted == False)  # noqa: E712

    async def get_active_by_user(self, user_id: uuid.UUID) -> Favorite | None:
        stmt = self._active_query().where(self.model.user_id == user_id)
        result = await self._session.scalars(stmt)
        return result.first()

    async def get_active_by_session(self, session_id: str) -> Favorite | None:
        stmt = self._active_query().where(self.model.session_id == session_id)
        result = await self._session.scalars(stmt)
        return result.first()

    async def get_or_create_for_user(self, user_id: uuid.UUID) -> Favorite:
        favorite = await self.get_active_by_user(user_id)
        if favorite:
            return favorite
        favorite = Favorite(user_id=user_id)
        self._session.add(favorite)
        await self._session.flush()
        return favorite

    async def get_or_create_for_session(self, session_id: str) -> Favorite:
        favorite = await self.get_active_by_session(session_id)
        if favorite:
            return favorite
        favorite = Favorite(session_id=session_id)
        self._session.add(favorite)
        await self._session.flush()
        return favorite

    async def get_favorite_item(
        self, favorite_id: uuid.UUID, product_id: int
    ) -> FavoriteProduct | None:
        stmt = select(FavoriteProduct).where(
            FavoriteProduct.favorite_id == favorite_id,
            FavoriteProduct.product_id == product_id,
        )
        result = await self._session.scalars(stmt)
        return result.first()

    async def add_product(
        self, favorite_id: uuid.UUID, product_id: int
    ) -> FavoriteProduct:
        existing = await self.get_favorite_item(favorite_id, product_id)
        if existing:
            return existing
        item = FavoriteProduct(favorite_id=favorite_id, product_id=product_id)
        self._session.add(item)
        await self._session.flush()
        return item

    async def remove_product(self, favorite_id: uuid.UUID, product_id: int) -> bool:
        existing = await self.get_favorite_item(favorite_id, product_id)
        if not existing:
            return False
        await self._session.delete(existing)
        await self._session.flush()
        return True

    async def get_products(self, favorite_id: uuid.UUID) -> list[Product]:
        stmt = (
            select(Product)
            .join(FavoriteProduct, Product.id == FavoriteProduct.product_id)
            .where(FavoriteProduct.favorite_id == favorite_id)
            .options(
                selectinload(Product.images),
                selectinload(Product.dimensions),
            )
        )
        result = await self._session.scalars(stmt)
        return list(result.all())

    async def soft_delete(self, favorite: Favorite) -> None:
        favorite.is_deleted = True
        favorite.deleted_at = datetime.now()
        await self._session.flush()

    async def assign_user(self, favorite: Favorite, user_id: uuid.UUID) -> None:
        favorite.user_id = user_id
        favorite.session_id = None
        await self._session.flush()

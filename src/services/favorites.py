import uuid

from fastapi import HTTPException

from src.database.models import Product
from src.schemas.favorites import FavoriteItemResponse, FavoritesResponse
from src.uow.sqlalchemy import UnitOfWork


class FavoritesService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_favorites(
        self,
        user_id: uuid.UUID | None = None,
        session_id: str | None = None,
    ) -> FavoritesResponse:
        favorite = await self._resolve_favorite(user_id, session_id)
        if not favorite:
            return FavoritesResponse(items=[], count=0)
        products = await self.uow.favorite_repo.get_products(favorite.id)
        return self._build_response(products)

    async def add(
        self,
        product_id: int,
        user_id: uuid.UUID | None = None,
        session_id: str | None = None,
    ) -> FavoritesResponse:
        product = await self.uow.product_repo.get_product(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        if user_id:
            favorite = await self.uow.favorite_repo.get_or_create_for_user(user_id)
        elif session_id:
            favorite = await self.uow.favorite_repo.get_or_create_for_session(session_id)
        else:
            raise HTTPException(status_code=400, detail="No user or session")

        await self.uow.favorite_repo.add_product(favorite.id, product_id)
        products = await self.uow.favorite_repo.get_products(favorite.id)
        return self._build_response(products)

    async def remove(
        self,
        product_id: int,
        user_id: uuid.UUID | None = None,
        session_id: str | None = None,
    ) -> FavoritesResponse:
        favorite = await self._resolve_favorite(user_id, session_id)
        if not favorite:
            raise HTTPException(status_code=404, detail="Favorites not found")

        removed = await self.uow.favorite_repo.remove_product(favorite.id, product_id)
        if not removed:
            raise HTTPException(status_code=404, detail="Product not in favorites")

        products = await self.uow.favorite_repo.get_products(favorite.id)
        return self._build_response(products)

    async def merge_on_login(
        self,
        user_id: uuid.UUID,
        session_id: str | None,
    ) -> None:
        if not session_id:
            return

        session_favorite = await self.uow.favorite_repo.get_active_by_session(session_id)
        if not session_favorite:
            return

        user_favorite = await self.uow.favorite_repo.get_active_by_user(user_id)
        if not user_favorite:
            await self.uow.favorite_repo.assign_user(session_favorite, user_id)
            return

        products = await self.uow.favorite_repo.get_products(session_favorite.id)
        for product in products:
            await self.uow.favorite_repo.add_product(user_favorite.id, product.id)

        await self.uow.favorite_repo.soft_delete(session_favorite)

    async def _resolve_favorite(
        self,
        user_id: uuid.UUID | None,
        session_id: str | None,
    ):
        if user_id:
            return await self.uow.favorite_repo.get_active_by_user(user_id)
        if session_id:
            return await self.uow.favorite_repo.get_active_by_session(session_id)
        return None

    @staticmethod
    def _build_response(products: list[Product]) -> FavoritesResponse:
        items = [
            FavoriteItemResponse(
                id=product.id,
                name=product.name,
                slug=product.slug,
                price=product.price,
            )
            for product in products
        ]
        return FavoritesResponse(items=items, count=len(items))

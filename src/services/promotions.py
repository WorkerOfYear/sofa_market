from fastapi import HTTPException

from src import schemas
from src.database.models import Product, Promotion
from src.uow.sqlalchemy import UnitOfWork


class PromotionsService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_promotions(self) -> list[Promotion]:
        return list(await self.uow.promotion_repo.get_all())

    async def get_promotion(self, promotion_id: int) -> Promotion:
        promotion = await self.uow.promotion_repo.get_by_id(promotion_id)
        if not promotion:
            raise HTTPException(status_code=404, detail="Promotion not found")
        return promotion

    async def create_promotion(self, data: schemas.PromotionCreate) -> Promotion:
        return await self.uow.promotion_repo.create(data)

    async def update_promotion(self, promotion_id: int, data: schemas.PromotionUpdate) -> Promotion:
        promotion = await self.uow.promotion_repo.update(promotion_id, data)
        if not promotion:
            raise HTTPException(status_code=404, detail="Promotion not found")
        return promotion

    async def delete_promotion(self, promotion_id: int) -> None:
        promotion = await self.get_promotion(promotion_id)
        await self.uow.promotion_repo.delete(promotion.id)

    async def apply_to_products(self, promotion_id: int, product_ids: list[int]) -> None:
        promotion = await self.get_promotion(promotion_id)
        await self.uow.promotion_repo.add_products(promotion.id, product_ids)

    async def remove_from_promotion(self, promotion_id: int, product_id: int) -> None:
        promotion = await self.get_promotion(promotion_id)
        await self.uow.promotion_repo.remove_product(
            promotion.id, product_id
        )

    async def get_promotion_products(self, promotion_id: int) -> list[Product]:
        promotion = await self.get_promotion(promotion_id)
        return list(
            await self.uow.promotion_repo.get_products(promotion.id)
        )

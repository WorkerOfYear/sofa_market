from typing import Sequence

from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src import schemas
from src.database.models import Product, Promotion, PromotionProduct

from .base import SQLAlchemyRepository


class PromotionsRepository(SQLAlchemyRepository[Promotion]):
    model = Promotion

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def get_all(self) -> Sequence[Promotion]:
        stmt = select(self.model).order_by(self.model.created_at.desc())
        result = await self._session.scalars(stmt)
        return result.all()

    async def get_by_id(self, promotion_id: int) -> Promotion | None:
        stmt = select(self.model).where(self.model.id == promotion_id)
        result = await self._session.scalars(stmt)
        return result.first()

    async def create(self, data: schemas.PromotionCreate) -> Promotion:
        promotion = self.model(**data.model_dump())
        self._session.add(promotion)
        await self._session.flush()
        await self._session.refresh(promotion)
        return promotion

    async def update(
        self, promotion_id: int, data: schemas.PromotionUpdate
    ) -> Promotion | None:
        promotion = await self.get_by_id(promotion_id)
        if not promotion:
            return None
        for key, value in data.model_dump(exclude_none=True).items():
            setattr(promotion, key, value)
        await self._session.flush()
        await self._session.refresh(promotion)
        return promotion

    async def delete(self, promotion_id: int) -> None:
        await self._delete(promotion_id)

    async def add_products(
        self, promotion_id: int, product_ids: list[int]
    ) -> None:
        values = [
            {"promotion_id": promotion_id, "product_id": pid}
            for pid in product_ids
        ]
        stmt = insert(PromotionProduct).values(values)
        stmt = stmt.on_conflict_do_nothing(
            index_elements=["promotion_id", "product_id"]
        )
        await self._session.execute(stmt)
        await self._session.flush()

    async def remove_product(
        self, promotion_id: int, product_id: int
    ) -> None:
        stmt = delete(PromotionProduct).where(
            PromotionProduct.promotion_id == promotion_id,
            PromotionProduct.product_id == product_id,
        )
        await self._session.execute(stmt)
        await self._session.flush()

    async def get_products(self, promotion_id: int) -> Sequence[Product]:
        stmt = (
            select(Product)
            .join(PromotionProduct, Product.id == PromotionProduct.product_id)
            .where(PromotionProduct.promotion_id == promotion_id)
            .options(
                selectinload(Product.images), selectinload(Product.dimensions)
            )
        )
        result = await self._session.scalars(stmt)
        return result.all()

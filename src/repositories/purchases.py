import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database.models import Cart, CartProduct, Product, Purchase, PurchaseProduct
from src.helpers.enums import PurchaseStatusEnum

from .base import SQLAlchemyRepository


class PurchasesRepository(SQLAlchemyRepository[Purchase]):
    model = Purchase

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def get_user_purchases(self, user_id: uuid.UUID) -> list[Purchase]:
        stmt = (
            select(Purchase)
            .where(Purchase.user_id == user_id)
            .order_by(Purchase.created_at.desc())
            .options(
                selectinload(Purchase.purchases_products).selectinload(
                    PurchaseProduct.product
                )
            )
        )
        result = await self._session.scalars(stmt)
        return list(result.all())

    async def get_purchase(
        self, purchase_id: int, user_id: uuid.UUID
    ) -> Purchase | None:
        stmt = (
            select(Purchase)
            .where(Purchase.id == purchase_id, Purchase.user_id == user_id)
            .options(
                selectinload(Purchase.purchases_products).selectinload(
                    PurchaseProduct.product
                )
            )
        )
        result = await self._session.scalars(stmt)
        return result.first()

    async def create_purchase(
        self, user_id: uuid.UUID, items: list[CartProduct]
    ) -> Purchase:
        purchase = Purchase(status=PurchaseStatusEnum.CREATED, user_id=user_id)
        self._session.add(purchase)
        await self._session.flush()

        for item in items:
            self._session.add(
                PurchaseProduct(
                    purchase_id=purchase.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                )
            )
        await self._session.flush()
        await self._session.refresh(purchase)
        return purchase

    async def soft_delete_cart(self, cart: Cart) -> None:
        cart.is_deleted = True
        cart.deleted_at = datetime.now()
        await self._session.flush()

    async def get_cart_items(self, cart_id: int) -> list[CartProduct]:
        stmt = (
            select(CartProduct)
            .where(CartProduct.cart_id == cart_id)
            .options(selectinload(CartProduct.product))
        )
        result = await self._session.scalars(stmt)
        return list(result.all())

    @staticmethod
    def calculate_total(items: list[CartProduct]) -> int:
        return sum(item.quantity * item.product.price for item in items)

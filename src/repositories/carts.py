import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database.models import Cart, CartProduct, Product

from .base import SQLAlchemyRepository


class CartsRepository(SQLAlchemyRepository[Cart]):
    model = Cart

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    def _active_cart_query(self):
        return select(self.model).where(self.model.is_deleted == False)

    async def get_by_user(self, user_id: uuid.UUID) -> Cart | None:
        stmt = (
            self._active_cart_query()
            .where(self.model.user_id == user_id)
            .options(
                selectinload(self.model.carts_products).selectinload(
                    CartProduct.product
                )
            )
        )
        result = await self._session.scalars(stmt)
        return result.first()

    async def get_by_session(self, session_id: str) -> Cart | None:
        stmt = (
            self._active_cart_query()
            .where(self.model.session_id == session_id)
            .options(
                selectinload(self.model.carts_products).selectinload(
                    CartProduct.product
                )
            )
        )
        result = await self._session.scalars(stmt)
        return result.first()

    async def create_for_user(self, user_id: uuid.UUID) -> Cart:
        cart = Cart(user_id=user_id, total_price=0)
        self._session.add(cart)
        await self._session.flush()
        return cart

    async def create_for_session(self, session_id: str) -> Cart:
        cart = Cart(session_id=session_id, total_price=0)
        self._session.add(cart)
        await self._session.flush()
        return cart

    async def get_cart_item(
        self, cart_id: int, product_id: int
    ) -> CartProduct | None:
        stmt = select(CartProduct).where(
            CartProduct.cart_id == cart_id,
            CartProduct.product_id == product_id,
        )
        result = await self._session.scalars(stmt)
        return result.first()

    async def add_product(
        self, cart_id: int, product_id: int, quantity: int = 1
    ) -> CartProduct:
        existing = await self.get_cart_item(cart_id, product_id)
        if existing:
            existing.quantity += quantity
            await self._session.flush()
            return existing

        item = CartProduct(
            cart_id=cart_id, product_id=product_id, quantity=quantity
        )
        self._session.add(item)
        await self._session.flush()
        return item

    async def update_quantity(
        self, cart_id: int, product_id: int, quantity: int
    ) -> CartProduct | None:
        item = await self.get_cart_item(cart_id, product_id)
        if not item:
            return None
        item.quantity = quantity
        await self._session.flush()
        return item

    async def remove_product(self, cart_id: int, product_id: int) -> bool:
        item = await self.get_cart_item(cart_id, product_id)
        if not item:
            return False
        await self._session.delete(item)
        await self._session.flush()
        return True

    async def soft_delete(self, cart: Cart) -> None:
        cart.is_deleted = True
        cart.deleted_at = datetime.now()
        await self._session.flush()

    async def assign_user(
        self, cart: Cart, user_id: uuid.UUID
    ) -> None:
        cart.user_id = user_id
        cart.session_id = None
        await self._session.flush()

    async def get_items_with_products(
        self, cart_id: int
    ) -> list[CartProduct]:
        stmt = (
            select(CartProduct)
            .where(CartProduct.cart_id == cart_id)
            .options(selectinload(CartProduct.product))
        )
        result = await self._session.scalars(stmt)
        return list(result.all())

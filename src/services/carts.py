import uuid

from fastapi import HTTPException

from src.database.models import CartProduct
from src.schemas.carts import CartItemResponse, CartResponse
from src.uow.sqlalchemy import UnitOfWork


class CartsService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_cart(
        self,
        user_id: uuid.UUID | None = None,
        session_id: str | None = None,
    ) -> CartResponse:
        cart = await self._resolve_cart(user_id, session_id)
        if not cart:
            return CartResponse(id=0, items=[], total_price=0, items_count=0)

        items = await self.uow.cart_repo.get_items_with_products(cart.id)
        return self._build_response(cart.id, items)

    async def add_to_cart(
        self,
        product_id: int,
        quantity: int,
        user_id: uuid.UUID | None = None,
        session_id: str | None = None,
    ) -> CartResponse:
        product = await self.uow.product_repo.get_product(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        cart = await self._resolve_cart(user_id, session_id)
        if not cart:
            if user_id:
                cart = await self.uow.cart_repo.create_for_user(user_id)
            elif session_id:
                cart = await self.uow.cart_repo.create_for_session(session_id)
            else:
                raise HTTPException(status_code=400, detail="No user or session")

        await self.uow.cart_repo.add_product(cart.id, product_id, quantity)

        items = await self.uow.cart_repo.get_items_with_products(cart.id)
        return self._build_response(cart.id, items)

    async def update_item_quantity(
        self,
        product_id: int,
        quantity: int,
        user_id: uuid.UUID | None = None,
        session_id: str | None = None,
    ) -> CartResponse:
        cart = await self._resolve_cart(user_id, session_id)
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")

        item = await self.uow.cart_repo.update_quantity(
            cart.id, product_id, quantity
        )
        if not item:
            raise HTTPException(
                status_code=404, detail="Product not in cart"
            )

        items = await self.uow.cart_repo.get_items_with_products(cart.id)
        return self._build_response(cart.id, items)

    async def remove_item(
        self,
        product_id: int,
        user_id: uuid.UUID | None = None,
        session_id: str | None = None,
    ) -> CartResponse:
        cart = await self._resolve_cart(user_id, session_id)
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")

        removed = await self.uow.cart_repo.remove_product(
            cart.id, product_id
        )
        if not removed:
            raise HTTPException(
                status_code=404, detail="Product not in cart"
            )

        items = await self.uow.cart_repo.get_items_with_products(cart.id)
        return self._build_response(cart.id, items)

    async def merge_on_login(
        self,
        user_id: uuid.UUID,
        session_id: str | None,
    ) -> None:
        """Merge anonymous session cart into user cart on login."""
        if not session_id:
            return

        session_cart = await self.uow.cart_repo.get_by_session(session_id)
        if not session_cart:
            return

        user_cart = await self.uow.cart_repo.get_by_user(user_id)

        if not user_cart:
            # No user cart: just assign user to the session cart
            await self.uow.cart_repo.assign_user(session_cart, user_id)
            return

        # Both exist: merge items from session cart into user cart
        session_items = await self.uow.cart_repo.get_items_with_products(
            session_cart.id
        )
        for item in session_items:
            await self.uow.cart_repo.add_product(
                user_cart.id, item.product_id, item.quantity
            )

        # Soft-delete the anonymous cart
        await self.uow.cart_repo.soft_delete(session_cart)

    async def _resolve_cart(self, user_id, session_id):
        if user_id:
            return await self.uow.cart_repo.get_by_user(user_id)
        if session_id:
            return await self.uow.cart_repo.get_by_session(session_id)
        return None

    @staticmethod
    def _build_response(cart_id: int, items: list[CartProduct]) -> CartResponse:
        cart_items = []
        total = 0
        for ci in items:
            subtotal = ci.product.price * ci.quantity
            total += subtotal
            cart_items.append(
                CartItemResponse(
                    product_id=ci.product_id,
                    product_name=ci.product.name,
                    product_slug=ci.product.slug,
                    product_price=ci.product.price,
                    quantity=ci.quantity,
                    subtotal=subtotal,
                )
            )
        return CartResponse(
            id=cart_id,
            items=cart_items,
            total_price=total,
            items_count=len(cart_items),
        )

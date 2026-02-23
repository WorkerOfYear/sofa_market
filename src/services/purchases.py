import uuid

from fastapi import HTTPException

from src.database.models import Purchase
from src.schemas.purchases import PurchaseItemResponse, PurchaseResponse
from src.uow.sqlalchemy import UnitOfWork


class PurchasesService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def checkout(self, user_id: uuid.UUID) -> PurchaseResponse:
        cart = await self.uow.cart_repo.get_by_user(user_id)
        if not cart:
            raise HTTPException(status_code=400, detail="Cart is empty")

        items = await self.uow.purchase_repo.get_cart_items(cart.id)
        if not items:
            raise HTTPException(status_code=400, detail="Cart is empty")

        purchase = await self.uow.purchase_repo.create_purchase(user_id, items)
        await self.uow.purchase_repo.soft_delete_cart(cart)
        purchase = await self.uow.purchase_repo.get_purchase(purchase.id, user_id)
        if not purchase:
            raise HTTPException(status_code=404, detail="Purchase not found")
        return self._map_purchase(purchase)

    async def get_my_purchases(self, user_id: uuid.UUID) -> list[PurchaseResponse]:
        purchases = await self.uow.purchase_repo.get_user_purchases(user_id)
        return [self._map_purchase(p) for p in purchases]

    async def get_purchase(self, purchase_id: int, user_id: uuid.UUID) -> PurchaseResponse:
        purchase = await self.uow.purchase_repo.get_purchase(purchase_id, user_id)
        if not purchase:
            raise HTTPException(status_code=404, detail="Purchase not found")
        return self._map_purchase(purchase)

    @staticmethod
    def _map_purchase(purchase: Purchase) -> PurchaseResponse:
        items: list[PurchaseItemResponse] = []
        total = 0

        for pp in purchase.purchases_products:
            subtotal = pp.quantity * pp.product.price
            total += subtotal
            items.append(
                PurchaseItemResponse(
                    product_id=pp.product_id,
                    product_name=pp.product.name,
                    product_slug=pp.product.slug,
                    product_price=pp.product.price,
                    quantity=pp.quantity,
                    subtotal=subtotal,
                )
            )

        return PurchaseResponse(
            id=purchase.id,
            status=purchase.status,
            created_at=purchase.created_at,
            items=items,
            total_price=total,
        )

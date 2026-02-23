from datetime import datetime

from src.helpers.enums import PurchaseStatusEnum

from .base import BaseSchema


class PurchaseItemResponse(BaseSchema):
    product_id: int
    product_name: str
    product_slug: str
    product_price: int
    quantity: int
    subtotal: int


class PurchaseResponse(BaseSchema):
    id: int
    status: PurchaseStatusEnum
    created_at: datetime
    items: list[PurchaseItemResponse]
    total_price: int


class PurchasesListResponse(BaseSchema):
    items: list[PurchaseResponse]

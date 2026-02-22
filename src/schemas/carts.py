from pydantic import Field

from .base import BaseSchema


class AddToCartPayload(BaseSchema):
    product_id: int
    quantity: int = Field(1, ge=1)


class UpdateQuantityPayload(BaseSchema):
    quantity: int = Field(ge=1)


class CartItemResponse(BaseSchema):
    product_id: int
    product_name: str
    product_slug: str
    product_price: int
    quantity: int
    subtotal: int


class CartResponse(BaseSchema):
    id: int
    items: list[CartItemResponse] = []
    total_price: int
    items_count: int

from datetime import datetime

from pydantic import Field

from .base import BaseSchema


class PromotionBase(BaseSchema):
    id: int
    name: str
    discount_percent: int
    valid_from: datetime | None = None
    valid_until: datetime | None = None
    created_at: datetime
    updated_at: datetime


class PromotionCreate(BaseSchema):
    name: str = Field(min_length=1, max_length=256)
    discount_percent: int = Field(ge=0, le=100)
    valid_from: datetime | None = None
    valid_until: datetime | None = None


class PromotionUpdate(BaseSchema):
    name: str | None = Field(None, max_length=256)
    discount_percent: int | None = Field(None, ge=0, le=100)
    valid_from: datetime | None = None
    valid_until: datetime | None = None


class ApplyProductsPayload(BaseSchema):
    product_ids: list[int] = Field(min_length=1)


class PromotionWithProducts(PromotionBase):
    products: list = []

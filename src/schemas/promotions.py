from datetime import datetime
from typing import Annotated

from pydantic import Field, AfterValidator

from .base import BaseSchema


def remove_timezone(v: datetime) -> datetime:
    """Remove timezone info to match TIMESTAMP WITHOUT TIME ZONE."""
    if v and isinstance(v, datetime) and v.tzinfo is not None:
        return v.replace(tzinfo=None)
    return v


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
    valid_from: Annotated[datetime | None, AfterValidator(remove_timezone)] = None
    valid_until: Annotated[datetime | None, AfterValidator(remove_timezone)] = None


class PromotionUpdate(BaseSchema):
    name: str | None = Field(None, max_length=256)
    discount_percent: int | None = Field(None, ge=0, le=100)
    valid_from: Annotated[datetime | None, AfterValidator(remove_timezone)] = None
    valid_until: Annotated[datetime | None, AfterValidator(remove_timezone)] = None


class ApplyProductsPayload(BaseSchema):
    product_ids: list[int] = Field(min_length=1)


class PromotionWithProducts(PromotionBase):
    products: list = []

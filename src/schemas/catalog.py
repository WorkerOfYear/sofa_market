from datetime import date, datetime

from pydantic import Field

from .base import BaseSchema
from .products import ImageBase, DimensionBase


class CategoryCatalogItem(BaseSchema):
    """Category in catalog with localized name."""

    id: int
    name: str
    slug: str
    created_at: date


class ProductCatalogItem(BaseSchema):
    """Product in catalog with localized name/description and promotion pricing."""

    id: int
    name: str
    slug: str
    description: str
    price: int
    current_price: int
    is_on_promotion: bool
    discount_percent: int
    category_id: int
    created_at: datetime
    updated_at: datetime
    images: list[ImageBase] = []
    dimensions: list[DimensionBase] = []


class ProductSearchResult(BaseSchema):
    items: list[ProductCatalogItem]
    total: int
    limit: int
    offset: int


class ProductCatalogFilters(BaseSchema):
    query: str | None = Field(None, description="Search in name/description")
    min_price: int | None = Field(None, ge=0)
    max_price: int | None = Field(None, ge=0)
    limit: int = Field(20, ge=1, le=100)
    offset: int = Field(0, ge=0)

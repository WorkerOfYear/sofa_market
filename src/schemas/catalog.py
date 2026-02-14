from datetime import date

from .base import BaseSchema
from .products import ImageBase, DimensionBase


class CategoryBase(BaseSchema):
    id: int
    name: str
    slug: str
    created_at: date


class ProductSearchResult(BaseSchema):
    items: list
    total: int
    limit: int
    offset: int

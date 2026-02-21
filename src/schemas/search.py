from pydantic import Field

from .base import BaseSchema


class AutocompleteQuery(BaseSchema):
    q: str = Field(min_length=1, max_length=200, description="Search query")
    limit: int = Field(5, ge=1, le=20, description="Max results per type")


class AutocompleteProduct(BaseSchema):
    id: int
    name: str
    slug: str
    price: int
    category_slug: str | None = None


class AutocompleteCategory(BaseSchema):
    id: int
    name: str
    slug: str


class AutocompleteResponse(BaseSchema):
    products: list[AutocompleteProduct] = []
    categories: list[AutocompleteCategory] = []

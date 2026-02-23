from .base import BaseSchema


class FavoriteItemResponse(BaseSchema):
    id: int
    name: str
    slug: str
    price: int


class FavoritesResponse(BaseSchema):
    items: list[FavoriteItemResponse] = []
    count: int

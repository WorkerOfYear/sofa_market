from datetime import datetime

from pydantic import Field, field_validator
from slugify import slugify

from .base import BaseSchema


class ImageBase(BaseSchema):
    id: int
    url: str


class DimensionBase(BaseSchema):
    id: int
    height: str
    width: str
    depth: str


class ProductCreate(BaseSchema):
    name: str = Field(min_length=1, max_length=256)
    description: str = Field(max_length=256)
    price: int = Field(gt=0)
    category_id: int
    slug: str | None = Field(None, max_length=256)

    @field_validator("slug", mode="before")
    @classmethod
    def generate_slug(cls, v: str | None, info) -> str:
        if not v and "name" in info.data:
            return slugify(info.data["name"])
        return v or ""


class ProductUpdate(BaseSchema):
    name: str | None = Field(None, max_length=256)
    description: str | None = Field(None, max_length=256)
    price: int | None = Field(None, gt=0)
    category_id: int | None = None


class ProductBase(BaseSchema):
    id: int
    name: str
    slug: str
    description: str
    price: int
    category_id: int
    created_at: datetime
    updated_at: datetime
    images: list[ImageBase] = []
    dimensions: list[DimensionBase] = []

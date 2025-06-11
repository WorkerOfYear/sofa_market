from datetime import datetime

from pydantic import BaseModel, HttpUrl, Field, field_validator
from slugify import slugify


class ImageSchema(BaseModel):
    id: int
    url: HttpUrl
    product_id: int

    class Config:
        from_attributes = True


class DimensionSchema(BaseModel):
    id: int
    height: str = Field(..., max_length=10)
    width: str = Field(..., max_length=10)
    depth: str = Field(..., max_length=10)
    product_id: int

    class Config:
        from_attributes = True


class ProductBaseSchema(BaseModel):
    name: str
    slug: str = Field(..., max_length=100)
    description: str
    price: int = Field(..., gt=0)
    category_id: int

    @field_validator("slug", mode="before")
    def generate_slug(cls, v, values):
        if not v and "name" in values:
            return slugify(values["name"])
        return v


class ProductCreateSchema(ProductBaseSchema):
    pass


class ProductUpdateSchema(ProductBaseSchema):
    name: str | None = None
    slug: str | None = Field(None, max_length=100)
    description: str | None = None
    price: int | None = Field(None, gt=0)
    category_id: int | None = None


class ProductSchema(ProductBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime
    images: list[ImageSchema] = []
    dimensions: list[DimensionSchema] = []

    class Config:
        from_attributes = True

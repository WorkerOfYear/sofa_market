"""Build Elasticsearch documents from ORM models."""

from __future__ import annotations

from typing import Any

from src.database.models import Category, Product


def product_to_doc(product: Product, category: Category | None = None) -> dict[str, Any]:
    doc = {
        "id": product.id,
        "name": product.name,
        "name_ru": product.name_ru,
        "name_kk": product.name_kk,
        "slug": product.slug,
        "description": product.description,
        "description_ru": product.description_ru,
        "description_kk": product.description_kk,
        "price": product.price,
        "category_id": product.category_id,
    }
    if category:
        doc["category_slug"] = category.slug
        doc["category_name"] = category.name
    return doc


def category_to_doc(category: Category) -> dict[str, Any]:
    return {
        "id": category.id,
        "name": category.name,
        "name_ru": category.name_ru,
        "name_kk": category.name_kk,
        "slug": category.slug,
    }

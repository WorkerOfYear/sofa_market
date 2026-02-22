"""
Bulk re-indexing script.

Usage:
    poetry run python -m src.search.reindex
"""

import asyncio
import logging

from elasticsearch import AsyncElasticsearch
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.config import settings
from src.database.connection import async_session_maker
from src.database.models import Category, Product
from src.search.documents import category_to_doc, product_to_doc
from src.search.service import SearchService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def reindex() -> None:
    es = AsyncElasticsearch(settings.ES_URL)
    search = SearchService(es)

    await search.ensure_indices()

    async with async_session_maker() as session:
        # Categories
        result = await session.execute(select(Category))
        categories = result.scalars().all()
        cat_map = {c.id: c for c in categories}

        cat_docs = [category_to_doc(c) for c in categories]
        await search.bulk_index_categories(cat_docs)

        # Products
        result = await session.execute(
            select(Product).options(
                selectinload(Product.images),
                selectinload(Product.dimensions),
            )
        )
        products = result.scalars().all()

        prod_docs = [
            product_to_doc(p, cat_map.get(p.category_id))
            for p in products
        ]
        await search.bulk_index_products(prod_docs)

    await es.close()
    logger.info(
        "Re-index complete: %d categories, %d products",
        len(cat_docs),
        len(prod_docs),
    )


if __name__ == "__main__":
    asyncio.run(reindex())

"""Elasticsearch search service with autocomplete."""

from __future__ import annotations

import logging
from typing import Any

from elasticsearch import AsyncElasticsearch, NotFoundError

from src.search.indices import (
    CATEGORIES_INDEX,
    CATEGORIES_MAPPING,
    PRODUCTS_INDEX,
    PRODUCTS_MAPPING,
)

logger = logging.getLogger(__name__)


class SearchService:
    def __init__(self, es: AsyncElasticsearch):
        self.es = es

    # ── Index management ───────────────────────────────────────────

    async def ensure_indices(self) -> None:
        for index, body in (
            (PRODUCTS_INDEX, PRODUCTS_MAPPING),
            (CATEGORIES_INDEX, CATEGORIES_MAPPING),
        ):
            if not await self.es.indices.exists(index=index):
                await self.es.indices.create(index=index, body=body)
                logger.info("Created ES index: %s", index)

    # ── Single-document operations ─────────────────────────────────

    async def index_product(self, product_doc: dict[str, Any]) -> None:
        await self.es.index(
            index=PRODUCTS_INDEX,
            id=str(product_doc["id"]),
            document=product_doc,
        )

    async def delete_product(self, product_id: int) -> None:
        try:
            await self.es.delete(index=PRODUCTS_INDEX, id=str(product_id))
        except NotFoundError:
            pass

    async def index_category(self, category_doc: dict[str, Any]) -> None:
        await self.es.index(
            index=CATEGORIES_INDEX,
            id=str(category_doc["id"]),
            document=category_doc,
        )

    async def delete_category(self, category_id: int) -> None:
        try:
            await self.es.delete(index=CATEGORIES_INDEX, id=str(category_id))
        except NotFoundError:
            pass

    # ── Bulk indexing ──────────────────────────────────────────────

    async def bulk_index_products(
        self, docs: list[dict[str, Any]]
    ) -> None:
        if not docs:
            return
        operations: list[dict] = []
        for doc in docs:
            operations.append({"index": {"_index": PRODUCTS_INDEX, "_id": str(doc["id"])}})
            operations.append(doc)
        await self.es.bulk(operations=operations, refresh=True)
        logger.info("Bulk indexed %d products", len(docs))

    async def bulk_index_categories(
        self, docs: list[dict[str, Any]]
    ) -> None:
        if not docs:
            return
        operations: list[dict] = []
        for doc in docs:
            operations.append({"index": {"_index": CATEGORIES_INDEX, "_id": str(doc["id"])}})
            operations.append(doc)
        await self.es.bulk(operations=operations, refresh=True)
        logger.info("Bulk indexed %d categories", len(docs))

    # ── Search / autocomplete ──────────────────────────────────────

    async def autocomplete(
        self,
        query: str,
        locale: str = "ru",
        limit: int = 5,
    ) -> dict[str, list[dict[str, Any]]]:
        """
        Search both products and categories indices.
        Returns {"products": [...], "categories": [...]}.
        """
        name_field = f"name_{locale}" if locale in ("ru", "kk") else "name"

        search_fields = [
            f"name^3",
            f"name_{locale}^3" if locale in ("ru", "kk") else None,
            "description",
            f"description_{locale}" if locale in ("ru", "kk") else None,
        ]
        search_fields = [f for f in search_fields if f]

        category_fields = [
            "name^3",
            f"name_{locale}^3" if locale in ("ru", "kk") else None,
        ]
        category_fields = [f for f in category_fields if f]

        product_results = await self._search_index(
            index=PRODUCTS_INDEX,
            query=query,
            fields=search_fields,
            size=limit,
        )

        category_results = await self._search_index(
            index=CATEGORIES_INDEX,
            query=query,
            fields=category_fields,
            size=limit,
        )

        return {
            "products": product_results,
            "categories": category_results,
        }

    async def _search_index(
        self,
        index: str,
        query: str,
        fields: list[str],
        size: int,
    ) -> list[dict[str, Any]]:
        body = {
            "size": size,
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": fields,
                    "type": "best_fields",
                    "fuzziness": "AUTO",
                },
            },
        }
        resp = await self.es.search(index=index, body=body)
        return [
            {**hit["_source"], "_score": hit["_score"]}
            for hit in resp["hits"]["hits"]
        ]

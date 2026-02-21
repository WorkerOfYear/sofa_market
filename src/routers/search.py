from fastapi import APIRouter, Depends

from src.dependencies import get_locale, get_search_service
from src.schemas.search import (
    AutocompleteCategory,
    AutocompleteProduct,
    AutocompleteResponse,
)
from src.search import SearchService

router = APIRouter(tags=["search"])


@router.get("/search", response_model=AutocompleteResponse)
async def search_autocomplete(
    q: str,
    limit: int = 5,
    search_service: SearchService = Depends(get_search_service),
    locale: str = Depends(get_locale),
):
    """Autocomplete search returning matching products and categories."""
    results = await search_service.autocomplete(
        query=q, locale=locale, limit=limit
    )

    products = [
        AutocompleteProduct(
            id=p["id"],
            name=p.get(f"name_{locale}") or p.get("name_ru") or p["name"],
            slug=p["slug"],
            price=p["price"],
            category_slug=p.get("category_slug"),
        )
        for p in results["products"]
    ]

    categories = [
        AutocompleteCategory(
            id=c["id"],
            name=c.get(f"name_{locale}") or c.get("name_ru") or c["name"],
            slug=c["slug"],
        )
        for c in results["categories"]
    ]

    return AutocompleteResponse(products=products, categories=categories)

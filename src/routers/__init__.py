from fastapi import APIRouter

from src.routers.auth import router as auth_router
from src.routers.catalog import router as catalog_router
from src.routers.products import router as products_router

router = APIRouter(prefix="/api/v1")

router.include_router(auth_router, prefix="/auth")
router.include_router(catalog_router, prefix="/catalog")
router.include_router(products_router, prefix="/product")

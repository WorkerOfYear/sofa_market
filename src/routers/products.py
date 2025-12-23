from fastapi import APIRouter, Depends

from src.dependencies import get_current_user
from src.schemas import ProductBase, UserBase

router = APIRouter(tags=["products"], dependencies=[Depends(get_current_user)])


@router.get("", response_model=list[ProductBase])
async def get_products():
    return
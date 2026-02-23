import uuid

from fastapi import APIRouter, Cookie, Depends, Response

from src.dependencies import get_current_user_optional, get_favorites_service
from src.schemas.favorites import FavoritesResponse
from src.schemas.users import UserBase
from src.services.favorites import FavoritesService

FAVORITE_COOKIE = "favorite_session"
FAVORITE_COOKIE_MAX_AGE = 60 * 60 * 24 * 30  # 30 days

router = APIRouter(tags=["favorites"])


def _ensure_session(response: Response, favorite_session: str | None) -> str:
    if favorite_session:
        return favorite_session
    new_id = uuid.uuid4().hex
    response.set_cookie(
        key=FAVORITE_COOKIE,
        value=new_id,
        max_age=FAVORITE_COOKIE_MAX_AGE,
        httponly=True,
    )
    return new_id


@router.get("", response_model=FavoritesResponse)
async def get_favorites(
    favorites_service: FavoritesService = Depends(get_favorites_service),
    user: UserBase | None = Depends(get_current_user_optional),
    favorite_session: str | None = Cookie(None),
):
    user_id = user.id if user else None
    return await favorites_service.get_favorites(
        user_id=user_id, session_id=favorite_session
    )


@router.post("/products/{product_id}", response_model=FavoritesResponse)
async def add_to_favorites(
    product_id: int,
    response: Response,
    favorites_service: FavoritesService = Depends(get_favorites_service),
    user: UserBase | None = Depends(get_current_user_optional),
    favorite_session: str | None = Cookie(None),
):
    user_id = user.id if user else None
    session_id = None if user_id else _ensure_session(response, favorite_session)
    return await favorites_service.add(
        product_id=product_id, user_id=user_id, session_id=session_id
    )


@router.delete("/products/{product_id}", response_model=FavoritesResponse)
async def remove_from_favorites(
    product_id: int,
    favorites_service: FavoritesService = Depends(get_favorites_service),
    user: UserBase | None = Depends(get_current_user_optional),
    favorite_session: str | None = Cookie(None),
):
    user_id = user.id if user else None
    return await favorites_service.remove(
        product_id=product_id, user_id=user_id, session_id=favorite_session
    )

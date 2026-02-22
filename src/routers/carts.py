import uuid

from fastapi import APIRouter, Cookie, Depends, Response

from src.dependencies import get_carts_service, get_current_user_optional
from src.schemas.carts import (
    AddToCartPayload,
    CartResponse,
    UpdateQuantityPayload,
)
from src.schemas.users import UserBase
from src.services.carts import CartsService

CART_COOKIE = "cart_session"
CART_COOKIE_MAX_AGE = 60 * 60 * 24 * 30  # 30 days

router = APIRouter(tags=["cart"])


def _ensure_session(
    response: Response,
    cart_session: str | None,
) -> str:
    """Return existing session_id or create one and set cookie."""
    if cart_session:
        return cart_session
    new_id = uuid.uuid4().hex
    response.set_cookie(
        key=CART_COOKIE,
        value=new_id,
        max_age=CART_COOKIE_MAX_AGE,
        httponly=True,
    )
    return new_id


@router.get("", response_model=CartResponse)
async def get_cart(
    carts_service: CartsService = Depends(get_carts_service),
    user: UserBase | None = Depends(get_current_user_optional),
    cart_session: str | None = Cookie(None),
):
    user_id = user.id if user else None
    return await carts_service.get_cart(
        user_id=user_id, session_id=cart_session
    )


@router.post("/items", response_model=CartResponse)
async def add_to_cart(
    payload: AddToCartPayload,
    response: Response,
    carts_service: CartsService = Depends(get_carts_service),
    user: UserBase | None = Depends(get_current_user_optional),
    cart_session: str | None = Cookie(None),
):
    user_id = user.id if user else None
    session_id = None if user_id else _ensure_session(response, cart_session)

    return await carts_service.add_to_cart(
        product_id=payload.product_id,
        quantity=payload.quantity,
        user_id=user_id,
        session_id=session_id,
    )


@router.patch("/items/{product_id}", response_model=CartResponse)
async def update_item_quantity(
    product_id: int,
    payload: UpdateQuantityPayload,
    carts_service: CartsService = Depends(get_carts_service),
    user: UserBase | None = Depends(get_current_user_optional),
    cart_session: str | None = Cookie(None),
):
    user_id = user.id if user else None
    return await carts_service.update_item_quantity(
        product_id=product_id,
        quantity=payload.quantity,
        user_id=user_id,
        session_id=cart_session,
    )


@router.delete("/items/{product_id}", response_model=CartResponse)
async def remove_item(
    product_id: int,
    carts_service: CartsService = Depends(get_carts_service),
    user: UserBase | None = Depends(get_current_user_optional),
    cart_session: str | None = Cookie(None),
):
    user_id = user.id if user else None
    return await carts_service.remove_item(
        product_id=product_id,
        user_id=user_id,
        session_id=cart_session,
    )

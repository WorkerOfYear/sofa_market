import secrets
import string

from redis.asyncio import Redis
from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, Request

from src.dependencies import (
    get_auth_service,
    get_carts_service,
    get_favorites_service,
    get_redis_client,
    get_sms_client,
)
from src.helpers.sms import SmsClient
from src.schemas import (
    EmailLoginPayload,
    EmailRegisterPayload,
    PhoneNumberPayload,
    UserBase,
    VerifyOTPayload,
)
from src.services.auth import AuthService
from src.services.carts import CartsService
from src.services.favorites import FavoritesService

router = APIRouter(tags=["auth"])


def generate_otp():
    return ''.join([secrets.choice(string.digits) for _ in range(6)])


@router.post("/send-otp")
async def send_otp(
        payload: PhoneNumberPayload,
        sms_client: SmsClient = Depends(get_sms_client),
        redis_client: Redis = Depends(get_redis_client)
):
    phone_number = payload.phone
    otp = generate_otp()
    redis_key = f"otp:{phone_number}"

    await redis_client.set(redis_key, otp, ex=300)
    await sms_client.send_sms(phone_number, otp)


@router.post("/verify-otp-and-login")
async def verify_otp_and_login(
        response: Response,
        payload: VerifyOTPayload,
        redis_client: Redis = Depends(get_redis_client),
        auth_service: AuthService = Depends(get_auth_service),
        carts_service: CartsService = Depends(get_carts_service),
        favorites_service: FavoritesService = Depends(get_favorites_service),
        cart_session: str | None = Cookie(None),
        favorite_session: str | None = Cookie(None),
):
    phone_number = payload.phone
    user_input_code = payload.otp_code

    redis_key = f"otp:{phone_number}"
    saved_code = await redis_client.get(redis_key)

    if saved_code is None:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    if saved_code == user_input_code:
        await redis_client.delete(redis_key)
        user = await auth_service.login(response, phone_number)
        await carts_service.merge_on_login(user.id, cart_session)
        await favorites_service.merge_on_login(user.id, favorite_session)
        return {"message": "OTP verified successfully, user logged in."}

    raise HTTPException(status_code=400, detail="Invalid OTP")


@router.post("/register", response_model=UserBase)
async def register(
    payload: EmailRegisterPayload,
    auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.register_email(str(payload.email), payload.password)


@router.post("/login", response_model=UserBase)
async def login(
    response: Response,
    payload: EmailLoginPayload,
    auth_service: AuthService = Depends(get_auth_service),
    carts_service: CartsService = Depends(get_carts_service),
    favorites_service: FavoritesService = Depends(get_favorites_service),
    cart_session: str | None = Cookie(None),
    favorite_session: str | None = Cookie(None),
):
    user = await auth_service.login_email(
        response, str(payload.email), payload.password
    )
    await carts_service.merge_on_login(user.id, cart_session)
    await favorites_service.merge_on_login(user.id, favorite_session)
    return user


@router.post("/logout")
async def logout(
        request: Request,
        response: Response,
        auth_service: AuthService = Depends(get_auth_service),
):
    await auth_service.logout(request, response)
    return {"message": "User logged out."}


@router.post("/profile", response_model=UserBase)
async def profile(
        request: Request,
        auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.get_current_user(request)

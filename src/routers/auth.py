import secrets
import string

from redis.asyncio import Redis
from fastapi import APIRouter, Depends, HTTPException, Response, Request

from src.dependencies.auth import get_auth_service
from src.dependencies.redis import get_redis_client
from src.dependencies.sms import get_sms_client
from src.schemas import PhoneNumberPayload, VerifyOTPayload, BaseUser
from src.helpers.sms import SmsClient
from src.services.auth import AuthService

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
        auth_service: AuthService = Depends(get_auth_service)
):
    phone_number = payload.phone
    user_input_code = payload.otp_code

    redis_key = f"otp:{phone_number}"
    saved_code = await redis_client.get(redis_key)

    if saved_code is None:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    if saved_code.decode("utf-8") == user_input_code:
        await redis_client.delete(redis_key)
        await auth_service.login(response, phone_number)
        return {"message": "OTP verified successfully, user logged in."}

    raise HTTPException(status_code=400, detail="Invalid OTP")


@router.post("/logout")
async def logout(
        request: Request,
        response: Response,
        auth_service: AuthService = Depends(get_auth_service),
):
    await auth_service.logout(request, response)
    return {"message": "User logged out."}


@router.post("/profile", response_model=BaseUser)
async def profile(
        request: Request,
        auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.get_current_user(request)

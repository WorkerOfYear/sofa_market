from fastapi import APIRouter

from src.schemas.users import UserReadSchema, UserCreateSchema
from src.auth.core import fastapi_users, auth_backend

router = APIRouter(tags=["auth"])

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="",
)

router.include_router(
    fastapi_users.get_register_router(UserReadSchema, UserCreateSchema),
    prefix="",
)

router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/reset-password",
)

router.include_router(
    fastapi_users.get_verify_router(UserReadSchema),
    prefix="/verify",
)

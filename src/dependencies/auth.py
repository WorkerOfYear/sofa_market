from fastapi import Depends, Request

from src.uow.sqlalchemy import UnitOfWork
from src.services.auth import AuthService
from src.auth import AuthManager, RedisStrategy, CookieTransport
from src.schemas import UserBase

from .uow import get_uow


async def get_redis_strategy(request: Request) -> RedisStrategy:
    return request.app.state.redis_strategy


async def get_cookie_transport(request: Request) -> CookieTransport:
    return request.app.state.cookie_transport


def get_auth_manager() -> AuthManager:
    return AuthManager()


async def get_auth_service(
    uow: UnitOfWork = Depends(get_uow),
    cookie_transport: CookieTransport = Depends(get_cookie_transport),
    redis_strategy: RedisStrategy = Depends(get_redis_strategy),
    auth_manager: AuthManager = Depends(get_auth_manager),
) -> AuthService:
    return AuthService(
        uow,
        cookie_transport,
        redis_strategy,
        auth_manager,
    )

async def get_current_user(
        request: Request,
        auth_service: AuthService = Depends(get_auth_service),
) -> UserBase:
    return await auth_service.get_current_user(request)

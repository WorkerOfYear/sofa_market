from fastapi import Depends, Request

from src.dependencies.uow import get_uow
from src.uow.sqlalchemy import UnitOfWork
from src.services.auth import AuthService
from src.auth import RedisStrategy, CookieTransport


async def get_redis_strategy(request: Request) -> RedisStrategy:
    return request.app.state.redis_strategy

async def get_cookie_transport(request: Request) -> CookieTransport:
    return request.app.state.cookie_transport


async def get_auth_service(
        uow: UnitOfWork = Depends(get_uow),
        cookie_transport: CookieTransport = Depends(get_cookie_transport),
        redis_strategy: RedisStrategy = Depends(get_redis_strategy),
):
    return AuthService(
        uow,
        cookie_transport,
        redis_strategy,
    )

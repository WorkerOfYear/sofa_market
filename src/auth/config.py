import redis.asyncio
from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users.authentication import CookieTransport, RedisStrategy, AuthenticationBackend
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.connection import get_async_session
from src.database.models import User

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

cookie_transport = CookieTransport(
    cookie_name="shop_token",
    cookie_max_age=3600,
    cookie_secure=False,
    cookie_httponly=True,
    cookie_samesite="lax"
)

redis = redis.from_url(
    "redis://localhost:6379",
    decode_responses=True
)


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


def get_redis_strategy() -> RedisStrategy:
    return RedisStrategy(
        redis,
        lifetime_seconds=3600
    )


auth_backend = AuthenticationBackend(
    name="redis_cookie",
    transport=cookie_transport,
    get_strategy=get_redis_strategy
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

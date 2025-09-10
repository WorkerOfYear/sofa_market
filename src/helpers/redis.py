import redis.asyncio as redis

from src.config import settings

redis_connection: redis.Redis | None = None


async def get_redis():
    global redis_connection
    if redis_connection is None:
        redis_connection = redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True
        )
    return redis_connection


async def close_redis():
    global redis_connection
    if redis_connection:
        await redis_connection.close()
        redis_connection = None

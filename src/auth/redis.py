import uuid
from datetime import datetime, timezone
from typing import Optional

import redis.asyncio as redis


class RedisStrategy:
    def __init__(self, redis_client: redis.Redis, lifetime_seconds: int = 3600):
        self.redis = redis_client
        self.lifetime_seconds = lifetime_seconds

    async def create_session(self, user_id: str) -> str:
        """Создание сессии в Redis"""
        session_id = str(uuid.uuid4())
        key = f"session:{session_id}"

        session_data = {
            "user_id": user_id,
            "created_at": datetime.now(timezone.utc),
        }

        # Сохраняем в Redis
        await self.redis.hset(key, mapping=session_data)
        await self.redis.expire(key, self.lifetime_seconds)

        return session_id

    async def get_session(self, session_id: str) -> Optional[dict]:
        """Получение сессии из Redis"""
        key = f"session:{session_id}"
        session_data = await self.redis.hgetall(key)

        if not session_data:
            return None

        # Обновляем TTL при каждом обращении
        await self.redis.expire(key, self.lifetime_seconds)

        return session_data

    async def delete_session(self, session_id: str):
        """Удаление сессии из Redis"""
        key = f"session:{session_id}"
        await self.redis.delete(key)

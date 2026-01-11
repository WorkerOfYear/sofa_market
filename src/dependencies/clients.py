import redis.asyncio as redis
from fastapi import Request

from src.helpers.sms import SmsClient
from src.helpers.storage import StorageClient


async def get_sms_client(request: Request) -> SmsClient:
    return request.app.state.sms_client


async def get_redis_client(request: Request) -> redis.Redis:
    return request.app.state.redis_client


async def get_storage_client(request: Request) -> StorageClient:
    return request.app.state.storage

import redis.asyncio as redis
from fastapi import Request

from src.helpers.sms import SmsClient
from src.helpers.storage import StorageClient
from src.search import SearchService


async def get_sms_client(request: Request) -> SmsClient:
    return request.app.state.sms_client


async def get_redis_client(request: Request) -> redis.Redis:
    return request.app.state.redis_client


async def get_storage_client(request: Request) -> StorageClient:
    return request.app.state.storage_client


async def get_search_service(request: Request) -> SearchService:
    return request.app.state.search_service

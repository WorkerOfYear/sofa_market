from contextlib import asynccontextmanager

import uvicorn
import redis.asyncio as redis
from elasticsearch import AsyncElasticsearch
from starlette.middleware.base import BaseHTTPMiddleware

from src.auth import CookieTransport, RedisStrategy
from src.config import settings
from src.core import CustomApp
from src.helpers.sms import MobizonClient
from src.helpers.storage import LocalStorageClient
from src.logger import logger
from src.middlewares import log_middleware
from src.routers import router
from src.search import SearchService


@asynccontextmanager
async def lifespan(app: CustomApp):
    app.state.redis_client = redis.from_url(
        settings.REDIS_URL,
        decode_responses=True
    )
    app.state.cookie_transport = CookieTransport(
        cookie_name=settings.AUTH_COOKIE_NAME,
        cookie_max_age=settings.SESSION_LIFETIME,
        cookie_secure=settings.ENVIRONMENT == "prod",
    )
    app.state.redis_strategy = RedisStrategy(
        app.state.redis_client,
        lifetime_seconds=settings.SESSION_LIFETIME
    )
    app.state.sms_client = MobizonClient(
        key=settings.MOBIZON_API_KEY
    )
    app.state.storage_client = LocalStorageClient(
        settings.LOCAL_STORAGE_PATH
    )
    
    app.state.es_client = AsyncElasticsearch(settings.ES_URL)
    app.state.search_service = SearchService(app.state.es_client)
    await app.state.search_service.ensure_indices()
    logger.info("Elasticsearch connected")

    yield

    await app.state.es_client.close()
    await app.state.redis_client.close()


app = CustomApp(title="marketplace", lifespan=lifespan)
logger.info("Starting API...")

app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)

app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8080,
        log_level="info",
    )

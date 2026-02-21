from typing import Optional

import redis.asyncio as redis
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI

from src.auth import CookieTransport, RedisStrategy
from src.helpers.sms import SmsClient
from src.search import SearchService


class AppState:
    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
        self.cookie_transport: Optional[CookieTransport] = None
        self.redis_strategy: Optional[RedisStrategy] = None
        self.sms_client: Optional[SmsClient] = None
        self.es_client: Optional[AsyncElasticsearch] = None
        self.search_service: Optional[SearchService] = None


class CustomApp(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state: AppState = AppState()

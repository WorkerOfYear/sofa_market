from typing import Optional

import redis.asyncio as redis
from fastapi import FastAPI

from src.helpers.sms import SmsClient
from src.auth import CookieTransport, RedisStrategy


class AppState:
    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
        self.cookie_transport: Optional[CookieTransport] = None
        self.redis_strategy: Optional[RedisStrategy] = None
        self.sms_client: Optional[SmsClient] = None


class CustomApp(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state: AppState = AppState()

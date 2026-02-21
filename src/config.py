from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENVIRONMENT: Literal["dev", "prod"] = "dev"

    POSTGRES_DB_NAME: str
    POSTGRES_TEST_DB_NAME: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    AUTH_SECRET_KEY: str
    AUTH_COOKIE_NAME: str
    SESSION_LIFETIME: int

    REDIS_HOST: str
    REDIS_PORT: str

    MOBIZON_API_KEY: str

    ELASTICSEARCH_URL: str = "http://localhost:9200"

    @property
    def DATABASE_URL(self):
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB_NAME}"
        )

    @property
    def TEST_DATABASE_URL(self):
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_TEST_DB_NAME}"
        )

    @property
    def REDIS_URL(self):
        return (
            f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"
        )

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

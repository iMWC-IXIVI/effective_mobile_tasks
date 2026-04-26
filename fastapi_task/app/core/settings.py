import redis.asyncio as redis

from contextlib import asynccontextmanager
from typing import Optional
from pathlib import Path

from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки проекта"""

    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    DATABASE_URL: str
    REDIS_URL: str

    _redis_client: Optional[redis.Redis] = None

    model_config = SettingsConfigDict(
        env_file=BASE_DIR.parent/'.env',
        extra='ignore'
    )

    @property
    def redis(self) -> redis.Redis:
        """Получение редис-клиента"""

        if self._redis_client is None:
            raise RuntimeError('Redis не инициализован')
        return self._redis_client

    async def initialize_redis(self) -> None:
        """Инициализация редис-клиента"""

        if self._redis_client is not None:
            return

        pool = redis.ConnectionPool.from_url(self.REDIS_URL, decode_responses=True)
        self._redis_client = redis.Redis(connection_pool=pool)

    async def close_redis_connect(self) -> None:
        """Закрытие соединения с редис-клиентом"""

        if not self._redis_client:
            return

        await self._redis_client.close()
        self._redis_client = None


settings = Settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Контроль запуска/завершения fastapi приложение"""

    await settings.initialize_redis()

    yield

    await settings.close_redis_connect()


async def get_redis() -> redis.Redis:
    """Зависимость для возвращения редис-клиента"""

    try:
        return settings.redis
    except RuntimeError:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, detail='Redis не инициализирован')

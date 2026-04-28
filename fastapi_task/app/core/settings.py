import logging
import sys
import redis.asyncio as redis

from datetime import datetime
from logging.handlers import RotatingFileHandler
from contextlib import asynccontextmanager
from typing import Optional
from pathlib import Path

from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger


class Settings(BaseSettings):
    """Настройки проекта"""

    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    LOG_DIR: Path = BASE_DIR/'logs'

    DATABASE_URL: str
    REDIS_URL: str

    SCHEDULER: AsyncIOScheduler = AsyncIOScheduler()

    _redis_client: Optional[redis.Redis] = None

    model_config = SettingsConfigDict(
        env_file=BASE_DIR.parent/'.env',
        extra='ignore'
    )

    @model_validator(mode='after')
    def _check_or_create_logs(self) -> 'Settings':
        """Проверка и создание папки logs"""

        if not self.LOG_DIR.exists():
            self.LOG_DIR.mkdir()
        return self

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

        await self._redis_client.aclose()
        self._redis_client = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Контроль запуска/завершения fastapi приложение"""

    setup_logger()  # Настройка логирования
    await settings.initialize_redis()  # Инициализация Redis'a
    settings.SCHEDULER.add_job(
        delete_data_from_redis,
        trigger=CronTrigger(hour=14, minute=11),
        name='delete_data_from_redis',
        misfire_grace_time=60*60,
        coalesce=True
    )  # Создание задачи на очистку данных
    settings.SCHEDULER.start()  # Запуск задачи

    yield

    settings.SCHEDULER.shutdown()  # Отключение задачи
    await settings.close_redis_connect()  # Закрытие redis соединения


async def get_redis() -> redis.Redis:
    """Зависимость для возвращения редис-клиента"""

    try:
        return settings.redis
    except RuntimeError as e:
        logging.error(f'Во время получения зависимости произошло исключение - {e}')
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, detail='Redis не инициализирован')


async def delete_data_from_redis() -> None:
    """Задача для очистки данных из редиса"""

    try:
        async_redis = settings.redis
        await async_redis.flushdb()
    except RuntimeError as e:
        logging.error(f'Произошла ошибка во время очистки данных - {e}')


def setup_logger() -> None:
    filename = datetime.now().strftime('%d-%m-%Y') + '.log'
    filepath = settings.LOG_DIR/filename

    console_formatter = logging.Formatter(
        fmt='%(asctime)s | %(name)s (%(levelname)s) - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_formatter = logging.Formatter(
        fmt='%(asctime)s | %(pathname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)

    file_handler = RotatingFileHandler(filename=filepath, mode='a', encoding='utf-8', maxBytes=10*1024*1024, backupCount=10)
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(file_formatter)

    logger = logging.getLogger()

    logger.setLevel(logging.INFO)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)


settings = Settings()

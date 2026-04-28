import pytest_asyncio

from httpx import ASGITransport, AsyncClient

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from asgi_lifespan import LifespanManager

from main import app
from core import settings


@pytest_asyncio.fixture(scope='function')
async def get_session():
    """Получение бд сессии"""

    engine = create_async_engine(settings.DATABASE_URL)
    async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        yield session


@pytest_asyncio.fixture(scope='function')
async def client():
    """Асинхронный клиент для тестирования"""

    async with LifespanManager(app) as manager:

        transport = ASGITransport(app=app)

        async with AsyncClient(transport=transport, base_url='http://localhost:8000') as client:
            yield client

import pytest_asyncio

from httpx import ASGITransport, AsyncClient

from main import app


@pytest_asyncio.fixture
async def client():
    """Асинхронный клиент для тестирования"""

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url='http://localhost:8000') as client:
        yield client

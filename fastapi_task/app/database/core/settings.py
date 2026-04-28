from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

from core import settings


engine = create_async_engine(url=settings.DATABASE_URL)

AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_connection():
    """Получение асинхронной сессии"""

    async with AsyncSessionLocal() as session:
        yield session


class Base(DeclarativeBase): pass

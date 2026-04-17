from core import settings

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase


async_engine = create_async_engine(settings.DATABASE_URL)

AsyncSessionLocal = async_sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    """Dependency injection для работы с ORM"""

    async with AsyncSessionLocal() as session:
        yield session


class Base(DeclarativeBase): pass

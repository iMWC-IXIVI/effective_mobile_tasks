import json
import redis.asyncio as redis

from fastapi import Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core import get_redis
from database.core import get_connection
from database.models import SpimexResults
from database.schemas import DateSchema


async def get_dates(
        last_days: int = 30,
        session: AsyncSession = Depends(get_connection),
        async_redis: redis.Redis = Depends(get_redis)
) -> list[DateSchema]:
    """Зависимость для получения списка дат торгов из редиса"""

    cache_name = f'trading:dates:last_days:{last_days}'
    cache = await async_redis.get(cache_name)

    if cache is None:
        result = await get_db_dates(last_days, session)
        cache_data = json.dumps([data.model_dump() for data in result], default=str)

        await async_redis.set(cache_name, cache_data)
    else:
        cache_data = json.loads(cache)
        result = [DateSchema(**item) for item in cache_data]

    return result


async def get_db_dates(
        last_days: int,
        session: AsyncSession
) -> list[DateSchema]:
    """Получения списка дат торгов из базы данных"""

    if last_days <= 0:
        return []

    query = select(SpimexResults.date).order_by(SpimexResults.date.desc()).limit(last_days)
    db_result = await session.execute(query)
    result = [DateSchema(date=dt) for dt in db_result.scalars().all()]

    return result

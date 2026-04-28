import logging
import json
import hashlib
import redis.asyncio as redis

from datetime import date
from typing import Sequence

from fastapi import Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core import get_redis
from database.core import get_connection
from database.models import SpimexResults


logger = logging.getLogger(__name__)


async def get_hash_params(
        start_date: date,
        end_date: date,
        oil_id: str,
        delivery_type_id: str,
        delivery_basis_id: str,
) -> str:
    """Получение hash параметров"""
    params = {
        'start_date': start_date,
        'end_date': end_date,
        'oil_id': oil_id,
        'delivery_type_id': delivery_type_id,
        'delivery_basis_id': delivery_basis_id
    }
    json_params = json.dumps(params, sort_keys=True, default=str).encode()
    hash_params = hashlib.sha256(json_params).hexdigest()

    return hash_params


async def get_dynamics(
        start_date: date,
        end_date: date,
        oil_id: str = None,
        delivery_type_id: str = None,
        delivery_basis_id: str = None,
        session: AsyncSession = Depends(get_connection),
        async_redis: redis.Redis = Depends(get_redis)
) -> list[SpimexResults]:
    """Зависимость для возвращения списка торгов с фильтрами из редиса"""

    hash_params = await get_hash_params(start_date, end_date, oil_id, delivery_type_id, delivery_basis_id)
    cache_name = f'trading:dynamics:{hash_params}'
    cache = await async_redis.get(cache_name)

    if cache is None:
        logger.info(f'CACHE MISSES данные не найдены в redis - {cache_name}')

        result = await get_db_dynamics(start_date, end_date, oil_id, delivery_type_id, delivery_basis_id, session)
        cache_data = json.dumps([item.to_dict() for item in result], default=str)

        await async_redis.set(cache_name, cache_data)
    else:
        logger.info(f'CACHE HITS данные найдены в redis - {cache_name}')

        cache_data = json.loads(cache)
        result = [SpimexResults(**item) for item in cache_data]

    return result


async def get_db_dynamics(
        start_date: date,
        end_date: date,
        oil_id: str,
        delivery_type_id: str,
        delivery_basis_id: str,
        session: AsyncSession
) -> Sequence[SpimexResults]:
    """Возвращение списка торгов с фильтрами из бд"""

    query = select(SpimexResults).where(SpimexResults.date >= start_date, SpimexResults.date <= end_date)

    if oil_id:
        query = query.where(SpimexResults.oil_id == oil_id)
    if delivery_type_id:
        query = query.where(SpimexResults.delivery_type_id == delivery_type_id)
    if delivery_basis_id:
        query = query.where(SpimexResults.delivery_basis_id == delivery_basis_id)

    db_result = await session.execute(query)
    result = db_result.scalars().all()

    return result

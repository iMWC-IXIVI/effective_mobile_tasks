import redis.asyncio as redis
import json
import hashlib

from typing import Sequence

from fastapi import Query, Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core import get_redis
from database.core import get_connection
from database.models import SpimexResults


async def get_hash_params(
        oil_id: str,
        delivery_type_id: str,
        delivery_basis_id: str,
        limit: int,
) -> str:
    """Получение hash параметров"""
    params = {
        'oil_id': oil_id,
        'delivery_type_id': delivery_type_id,
        'delivery_basis_id': delivery_basis_id,
        'limit': limit
    }
    json_params = json.dumps(params, sort_keys=True, default=str).encode()
    hash_params = hashlib.sha256(json_params).hexdigest()

    return hash_params


async def get_results(
        oil_id: str = None,
        delivery_type_id: str = None,
        delivery_basis_id: str = None,
        limit: int = Query(100, ge=100, le=1000),
        session: AsyncSession = Depends(get_connection),
        async_redis: redis.Redis = Depends(get_redis)
) -> list[SpimexResults]:
    """Зависимость для возвращения списка последних торгов с фильтрацией из редиса"""

    hash_params = await get_hash_params(oil_id, delivery_type_id, delivery_basis_id, limit)
    cache_name = f'trading:results:{hash_params}'

    cache = await async_redis.get(cache_name)

    if cache is None:
        result = await get_db_results(oil_id, delivery_type_id, delivery_basis_id, limit, session)
        cache_data = json.dumps([item.to_dict() for item in result], default=str)

        await async_redis.set(cache_name, cache_data)
    else:
        cache_data = json.loads(cache)
        result = [SpimexResults(**item) for item in cache_data]

    return result


async def get_db_results(
        oil_id: str,
        delivery_type_id: str,
        delivery_basis_id: str,
        limit: int,
        session: AsyncSession
) -> Sequence[SpimexResults]:
    """Возвращение списка последних торгов с фильтрацией из бд"""

    query = select(SpimexResults)

    if oil_id:
        query = query.where(SpimexResults.oil_id == oil_id)
    if delivery_type_id:
        query = query.where(SpimexResults.delivery_type_id == delivery_type_id)
    if delivery_basis_id:
        query = query.where(SpimexResults.delivery_basis_id == delivery_basis_id)

    query = query.order_by(SpimexResults.date.desc()).limit(limit)

    db_result = await session.execute(query)
    result = db_result.scalars().all()

    return result

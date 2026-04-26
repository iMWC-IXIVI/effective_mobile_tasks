from typing import Sequence

from fastapi import Query, Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.core import get_connection
from database.models import SpimexResults


async def get_results(
        oil_id: str = None,
        delivery_type_id: str = None,
        delivery_basis_id: str = None,
        limit: int = Query(100, ge=100, le=1000),
        session: AsyncSession = Depends(get_connection)
) -> Sequence[SpimexResults]:
    """Зависимость для возвращения списка последних торгов с фильтрацией"""

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

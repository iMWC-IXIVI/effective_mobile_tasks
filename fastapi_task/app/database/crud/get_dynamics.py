from datetime import date
from typing import Sequence

from fastapi import Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.core import get_connection
from database.models import SpimexResults


async def get_dynamics(
        start_date: date,
        end_date: date,
        oil_id: str = None,
        delivery_type_id: str = None,
        delivery_basis_id: str = None,
        session: AsyncSession = Depends(get_connection)
) -> Sequence[SpimexResults]:
    """Зависимость для возвращения списка торгов с фильтрами"""

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

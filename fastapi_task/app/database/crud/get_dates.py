from fastapi import Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.core import get_connection
from database.models import SpimexResults
from database.schemas import DateSchema


async def get_dates(
        last_days: int = 30,
        session: AsyncSession = Depends(get_connection)
) -> list[DateSchema]:
    """Зависимость для получения списка дат торгов"""

    if last_days <= 0:
        return []

    query = select(SpimexResults.date).order_by(SpimexResults.date.desc()).limit(last_days)
    db_result = await session.execute(query)
    result = [DateSchema(date=dt) for dt in db_result.scalars().all()]

    return result

from fastapi import APIRouter, Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.core import get_connection
from database.models import SpimexResults
from database.schemas import DateSchema


trading_router = APIRouter(
    prefix='/api/v1/trading',
    tags=['Торговля', ]
)


@trading_router.get(
    '/dates',
    summary='Список дат',
    description='Возвращает список дат последних торговых дней с возможностью фильтрации по количеству последних дней'
)
async def get_last_trading_dates(
        last_days: int = 30,
        session: AsyncSession = Depends(get_connection),
) -> list[DateSchema]:
    """Возвращение списка дат торгов"""

    if last_days <= 0:
        return []

    query = select(SpimexResults.date).limit(last_days)
    db_result = await session.execute(query)
    result = [DateSchema(date=dt) for dt in db_result.scalars().all()]

    return result

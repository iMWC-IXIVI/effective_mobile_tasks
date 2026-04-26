from datetime import date

from fastapi import APIRouter, Depends, Query

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.core import get_connection
from database.models import SpimexResults
from database.schemas import DateSchema, SpimexSchema


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


@trading_router.get(
    '/dynamics',
    summary='Список торгов',
    description='Возвращает список торгов за заданный период с возможностью фильтрации по различным параметрам.'
)
async def get_dynamics(
        start_date: date,
        end_date: date,
        oil_id: str = None,
        delivery_type_id: str = None,
        delivery_basis_id: str = None,
        session: AsyncSession = Depends(get_connection)
) -> list[SpimexSchema]:
    """Возвращение списка торгов с фильтрами"""

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


@trading_router.get(
    '/results',
    summary='Список последни торгов',
    description='Возвращает список последних торгов с возможностью фильтрации по характеристикам продукта'
)
async def get_trading_results(
        oil_id: str = None,
        delivery_type_id: str = None,
        delivery_basis_id: str = None,
        limit: int = Query(100, ge=100, le=1000),
        session: AsyncSession = Depends(get_connection)
) -> list[SpimexSchema]:
    """Возвращение списка последних торгов с фильтрацией"""

    query = select(SpimexResults).limit(limit)

    if oil_id:
        query = query.where(SpimexResults.oil_id == oil_id)
    if delivery_type_id:
        query = query.where(SpimexResults.delivery_type_id == delivery_type_id)
    if delivery_basis_id:
        query = query.where(SpimexResults.delivery_basis_id == delivery_basis_id)

    db_result = await session.execute(query)
    result = db_result.scalars().all()

    return result

# TODO посмотреть в сторону "ПОСЛЕДНИХ ТОРГОВ ПО ДНЯМ" сортировка везде относительно сегодняшнего дня!!!!!

from typing import Sequence

from fastapi import APIRouter, Depends

from database.crud import get_dates, get_dynamics, get_results
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
        result: list[DateSchema] = Depends(get_dates)
) -> list[DateSchema]:
    """Возвращение списка дат торгов"""

    return result


@trading_router.get(
    '/dynamics',
    summary='Список торгов',
    description='Возвращает список торгов за заданный период с возможностью фильтрации по различным параметрам.'
)
async def get_dynamics(
        result: Sequence[SpimexResults] = Depends(get_dynamics)
) -> list[SpimexSchema]:
    """Возвращение списка торгов с фильтрами"""

    return result


@trading_router.get(
    '/results',
    summary='Список последни торгов',
    description='Возвращает список последних торгов с возможностью фильтрации по характеристикам продукта'
)
async def get_trading_results(
        result: Sequence[SpimexResults] = Depends(get_results)
) -> list[SpimexSchema]:
    """Возвращение списка последних торгов с фильтрацией"""

    return result

import pytest

from database.crud import get_db_dates


@pytest.mark.asyncio
@pytest.mark.parametrize('last_days', [-1, 0])
async def test_check_le_0_get_dates(last_days: int):
    """Проверка рузльтат в случае есть last_days <= 0"""

    result = await get_db_dates(last_days, None)

    assert result == []

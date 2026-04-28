import time
import asyncio
import httpx

from database.crud import get_db_dates
from database.schemas import DateSchema


base_url = '/api/v1/trading/dates'


async def test_get_dates(client: httpx.AsyncClient) -> None:
    """Тестирование /api/v1/trading/dates"""

    response = await client.get(base_url)
    data = response.json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) <= 30


async def test_get_dates_broken(client: httpx.AsyncClient) -> None:
    """Тестирование put, post, patch, delete"""

    responses = await asyncio.gather(*[
        client.post(base_url),
        client.put(base_url),
        client.patch(base_url),
        client.delete(base_url)
    ])
    responses_status = [response.status_code for response in responses]
    responses_data = [response.json() for response in responses]

    assert responses_status == [405, 405, 405, 405]
    assert responses_data == [{'detail': 'Method Not Allowed'} for _ in range(4)]


async def test_get_dates_last_days(client: httpx.AsyncClient) -> None:
    """Тестирование с флагом last_days"""

    response1 = await client.get(base_url + '?last_days=150')
    data1 = response1.json()

    response2 = await client.get(base_url + '?last_days=-50')
    data2 = response2.json()

    assert response1.status_code == 200
    assert isinstance(data1, list)
    assert len(data1) <= 150

    assert response2.status_code == 200
    assert isinstance(data2, list)
    assert len(data2) == 0


async def test_get_dates_cache(client: httpx.AsyncClient) -> None:
    """Тестирование на сохранение в кэш"""

    start = time.perf_counter()
    response1 = await client.get(base_url + '?last_days=5')
    first_time = time.perf_counter() - start

    start = time.perf_counter()
    response2 = await client.get(base_url + '?last_days=5')
    second_time = time.perf_counter() - start

    assert response1.status_code == 200 and response2.status_code == 200
    assert response1.json() == response2.json()
    assert second_time <= first_time


async def test_get_db_dates(get_session) -> None:
    """Получение данных из бд напрямую"""

    last_days = 30
    result = await get_db_dates(last_days, get_session)

    for data in result:
        assert isinstance(data, DateSchema)
        assert hasattr(data, 'date')

    assert len(result) <= last_days

import pytest

from fastapi.testclient import TestClient

from main import app
from core import get_redis
from database.core import get_connection


trading_url = f'/api/v1/trading/dates'


@pytest.mark.integration
@pytest.mark.parametrize('last_days, return_counter', [[30, 10], [20, 10], [5, 5]])
def test_check_dates_redis_miss(last_days: int, return_counter: int, create_data, mock_redis_cache_miss, async_session):
    """Тестирование получение дат с redis miss"""

    app.dependency_overrides[get_connection] = lambda: async_session
    app.dependency_overrides[get_redis] = lambda: mock_redis_cache_miss

    cache_name = f'trading:dates:last_days:{last_days}'

    with TestClient(app) as client:
        response = client.get(f'{trading_url}?last_days={last_days}')

    assert response.status_code == 200
    mock_redis_cache_miss.get.assert_called_once_with(cache_name)
    mock_redis_cache_miss.set.assert_called_once()
    assert len(response.json()) == return_counter

    app.dependency_overrides.clear()


@pytest.mark.integration
@pytest.mark.parametrize('last_days, return_counter', [[30, 10], [20, 10], [5, 5]])
def test_check_dates_redis_hit(last_days: int, return_counter: int, create_data, mock_redis_cache_dates_hit, async_session):
    """Тестирование получение дат с redis hit"""

    app.dependency_overrides[get_connection] = lambda: async_session
    app.dependency_overrides[get_redis] = lambda: mock_redis_cache_dates_hit

    cache_name = f'trading:dates:last_days:{last_days}'

    with TestClient(app) as client:
        response = client.get(f'{trading_url}?last_days={last_days}')

    assert response.status_code == 200
    mock_redis_cache_dates_hit.get.assert_called_once_with(cache_name)
    mock_redis_cache_dates_hit.set.assert_not_called()
    assert len(response.json()) == return_counter

    app.dependency_overrides.clear()

import pytest

from fastapi.testclient import TestClient


@pytest.mark.integration
def test_check_health_url(client_test_cache_miss: TestClient):
    """Тестирование работоспособности"""

    response = client_test_cache_miss.get('/api/v1/routers/test/ping')

    assert response.status_code == 200
    assert response.json() == {'message': 'pong'}


@pytest.mark.integration
@pytest.mark.parametrize('last_days', [30, 20, 5])
def test_check_dates_cache_miss(last_days: int, client_test_cache_miss: TestClient, create_data, mock_redis_cache_miss):
    """Тестирование получения дат при redis cache miss"""

    cache_name = f'trading:dates:last_days:{last_days}'

    response = client_test_cache_miss.get(f'/api/v1/trading/dates?last_days={last_days}')
    counter_data = len(response.json())

    mock_redis_cache_miss.get.assert_called_once_with(cache_name)
    mock_redis_cache_miss.set.assert_called_once()

    assert response.status_code == 200

    if last_days == 5:
        assert counter_data == 5
    else:
        assert counter_data == 10


@pytest.mark.integration
@pytest.mark.parametrize('last_days', [30, 20, 5])
def test_check_dates_cache_hit(last_days: int, client_test_cache_hit: TestClient, create_data, mock_redis_cache_hit):
    """Тестирование получения дат при redis cache hit"""

    cache_name = f'trading:dates:last_days:{last_days}'

    response = client_test_cache_hit.get(f'/api/v1/trading/dates?last_days={last_days}')
    counter_data = len(response.json())

    mock_redis_cache_hit.get.assert_called_once_with(cache_name)

    assert response.status_code == 200

    if last_days == 5:
        assert counter_data == 5
    else:
        assert counter_data == 10

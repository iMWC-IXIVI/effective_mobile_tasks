import pytest

from datetime import date

from fastapi.testclient import TestClient

from main import app
from core import get_redis
from database.core import get_connection
from database.crud import get_hash_params_dynamics


url = '/api/v1/trading/dynamics'


@pytest.mark.asyncio
@pytest.mark.integration
@pytest.mark.parametrize('start_date, end_date, oil_id, delivery_type_id, delivery_basis_id, return_counter', [
    [date(year=2026, month=3, day=1), date(year=2026, month=3, day=5), None, None, None, 5],
    [date(year=2026, month=3, day=1), date(year=2026, month=3, day=10), None, None, None, 10],
    [date(year=2026, month=3, day=1), date(year=2026, month=3, day=5), 'AST_20', 'Street_50', 'st.50', 1],
    [date(year=2026, month=3, day=1), date(year=2026, month=3, day=1), 'AST_21', 'Street_55', 'st.60', 0]
])
async def test_check_dynamics_redis_miss(
        start_date: date,
        end_date: date,
        oil_id: str | None,
        delivery_type_id: str | None,
        delivery_basis_id: str | None,
        return_counter: int,
        create_data,
        mock_redis_cache_miss,
        async_session
):
    app.dependency_overrides[get_connection] = lambda: async_session
    app.dependency_overrides[get_redis] = lambda: mock_redis_cache_miss

    hash_params = await get_hash_params_dynamics(start_date, end_date, oil_id, delivery_type_id, delivery_basis_id)
    cache_name = f'trading:dynamics:{hash_params}'

    params = f'start_date={start_date}&end_date={end_date}'

    if oil_id:
        params += f'&oil_id={oil_id}'
    if delivery_type_id:
        params += f'&delivery_type_id={delivery_type_id}'
    if delivery_basis_id:
        params += f'&delivery_basis_id={delivery_basis_id}'

    with TestClient(app) as client:
        response = client.get(f'{url}?{params}')

    assert response.status_code == 200
    mock_redis_cache_miss.get.assert_called_once_with(cache_name)
    mock_redis_cache_miss.set.assert_called_once()
    assert len(response.json()) == return_counter

    app.dependency_overrides.clear()


@pytest.mark.asyncio
@pytest.mark.integration
@pytest.mark.parametrize('start_date, end_date, oil_id, delivery_type_id, delivery_basis_id, return_counter', [
    [date(year=2026, month=3, day=1), date(year=2026, month=3, day=5), None, None, None, 5],
    [date(year=2026, month=3, day=1), date(year=2026, month=3, day=10), None, None, None, 10],
    [date(year=2026, month=3, day=1), date(year=2026, month=3, day=5), 'AST_20', 'Street_50', 'st.50', 1],
    [date(year=2026, month=3, day=1), date(year=2026, month=3, day=1), 'AST_21', 'Street_55', 'st.60', 0]
])
async def test_check_dynamics_redis_hit(
        start_date: date,
        end_date: date,
        oil_id: str | None,
        delivery_type_id: str | None,
        delivery_basis_id: str | None,
        return_counter: int,
        create_data,
        mock_redis_cache_dynamics_hit,
        async_session
):
    app.dependency_overrides[get_connection] = lambda: async_session
    app.dependency_overrides[get_redis] = lambda: mock_redis_cache_dynamics_hit

    hash_params = await get_hash_params_dynamics(start_date, end_date, oil_id, delivery_type_id, delivery_basis_id)
    cache_name = f'trading:dynamics:{hash_params}'

    params = f'start_date={start_date}&end_date={end_date}'

    if oil_id:
        params += f'&oil_id={oil_id}'
    if delivery_type_id:
        params += f'&delivery_type_id={delivery_type_id}'
    if delivery_basis_id:
        params += f'&delivery_basis_id={delivery_basis_id}'

    with TestClient(app) as client:
        response = client.get(f'{url}?{params}')

    assert response.status_code == 200
    mock_redis_cache_dynamics_hit.get.assert_called_once_with(cache_name)
    mock_redis_cache_dynamics_hit.set.assert_not_called()
    assert len(response.json()) == return_counter

    app.dependency_overrides.clear()

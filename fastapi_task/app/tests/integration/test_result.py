import pytest

from fastapi.testclient import TestClient

from main import app
from core import get_redis
from database.core import get_connection
from database.crud import get_hash_params_results


url = '/api/v1/trading/results'


@pytest.mark.asyncio
@pytest.mark.integration
@pytest.mark.parametrize('oil_id, delivery_type_id, delivery_basis_id, limit, return_counter', [
    [None, None, None, 100, 10],
    ['AST_20', 'Street_50', 'st.50', 100, 1],
    ['AST_20', 'Street_55', 'st.70', 150, 0]
])
async def test_check_results_redis_miss(
        oil_id: str | None,
        delivery_type_id: str | None,
        delivery_basis_id: str | None,
        limit: int,
        return_counter: int,
        create_data,
        async_session,
        mock_redis_cache_miss
):
    """Тестирование получение результатов с redis miss"""

    app.dependency_overrides[get_connection] = lambda: async_session
    app.dependency_overrides[get_redis] = lambda: mock_redis_cache_miss

    hash_params = await get_hash_params_results(oil_id, delivery_type_id, delivery_basis_id, limit)
    cache_name = f'trading:results:{hash_params}'

    params = f'limit={limit}'

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
@pytest.mark.parametrize('oil_id, delivery_type_id, delivery_basis_id, limit, return_counter', [
    [None, None, None, 100, 10],
    ['AST_20', 'Street_50', 'st.50', 100, 1],
    ['AST_20', 'Street_55', 'st.70', 150, 0]
])
async def test_check_results_redis_hit(
        oil_id: str | None,
        delivery_type_id: str | None,
        delivery_basis_id: str | None,
        limit: int,
        return_counter: int,
        create_data,
        async_session,
        mock_redis_cache_results_hit
):
    """Тестирование получение результатов с redis miss"""

    app.dependency_overrides[get_connection] = lambda: async_session
    app.dependency_overrides[get_redis] = lambda: mock_redis_cache_results_hit

    hash_params = await get_hash_params_results(oil_id, delivery_type_id, delivery_basis_id, limit)
    cache_name = f'trading:results:{hash_params}'

    params = f'limit={limit}'

    if oil_id:
        params += f'&oil_id={oil_id}'
    if delivery_type_id:
        params += f'&delivery_type_id={delivery_type_id}'
    if delivery_basis_id:
        params += f'&delivery_basis_id={delivery_basis_id}'

    with TestClient(app) as client:
        response = client.get(f'{url}?{params}')

    assert response.status_code == 200
    mock_redis_cache_results_hit.get.assert_called_once_with(cache_name)
    mock_redis_cache_results_hit.set.assert_not_called()
    assert len(response.json()) == return_counter

    app.dependency_overrides.clear()

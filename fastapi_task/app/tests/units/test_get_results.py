import pytest

from database.crud import get_hash_params_results


@pytest.mark.asyncio
@pytest.mark.unit
@pytest.mark.parametrize('oil_id, delivery_type_id, delivery_basis_id, limit', [
    ['AST', 'Street', 'st.100', 50],
    ['ASC', 'StreetFood', 'st.100', 50],
    ['ASC', 'Street', 'mb.100', 50],
    ['ASC', 'Street', 'st.100', 100],
])
async def test_check_hash_params_results(
        oil_id: str,
        delivery_type_id: str,
        delivery_basis_id: str,
        limit: int
):
    """Проверка на правильную генерацию hash в results"""

    valid_data = {
        'oil_id': 'ASC',
        'delivery_type_id': 'Street',
        'delivery_basis_id': 'st.100',
        'limit': 50
    }

    valid_hash = await get_hash_params_results(**valid_data)
    invalid_hash = await get_hash_params_results(oil_id, delivery_type_id, delivery_basis_id, limit)

    assert valid_hash != invalid_hash

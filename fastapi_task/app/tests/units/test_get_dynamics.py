import pytest

from datetime import date

from database.crud import get_hash_params_dynamics


@pytest.mark.asyncio
@pytest.mark.unit
@pytest.mark.parametrize('start_date, end_date, oil_id, delivery_type_id, delivery_basis_id', [
    [date(year=2025, month=1, day=3), date(year=2025, month=1, day=2), 'ASC', 'Street', 'st.100'],
    [date(year=2025, month=1, day=1), date(year=2025, month=1, day=3), 'ASC', 'Street', 'st.100'],
    [date(year=2025, month=1, day=1), date(year=2025, month=1, day=2), 'AST', 'Street', 'st.100'],
    [date(year=2025, month=1, day=1), date(year=2025, month=1, day=2), 'ASC', 'StreetFood', 'st.100'],
    [date(year=2025, month=1, day=1), date(year=2025, month=1, day=2), 'ASC', 'Street', 'mb.100'],
])
async def test_check_hash_params_dynamics(
        start_date: date,
        end_date: date,
        oil_id: str,
        delivery_type_id: str,
        delivery_basis_id: str
):
    """Проверка на правильную генерацию hash в dynamics"""

    valid_data = {
        'start_date': date(year=2025, month=1, day=1),
        'end_date': date(year=2025, month=1, day=2),
        'oil_id': 'ASC',
        'delivery_type_id': 'Street',
        'delivery_basis_id': 'st.100'
    }

    valid_hash = await get_hash_params_dynamics(**valid_data)
    invalid_hash = await get_hash_params_dynamics(start_date, end_date, oil_id, delivery_type_id, delivery_basis_id)

    assert valid_hash != invalid_hash

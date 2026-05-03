import pytest
import pytest_asyncio

from pytest_mock import MockerFixture

from datetime import date
from decimal import Decimal

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from database.crud import get_hash_params_dynamics
from database.core import Base
from database.models import SpimexResults


redis_data_dates_10 = '''
[
{"date": "2026-03-01", "oil_id": "AST_20", "delivery_type_id": "Street_50", "delivery_basis_id": "st.50", "volume": "10000", "total": "100000.54321", "count": 5}, 
{"date": "2026-03-02", "oil_id": "AST_21", "delivery_type_id": "Street_51", "delivery_basis_id": "st.51", "volume": "10001", "total": "100001.54321", "count": 6}, 
{"date": "2026-03-03", "oil_id": "AST_22", "delivery_type_id": "Street_52", "delivery_basis_id": "st.52", "volume": "10002", "total": "100002.54321", "count": 7}, 
{"date": "2026-03-04", "oil_id": "AST_23", "delivery_type_id": "Street_53", "delivery_basis_id": "st.53", "volume": "10003", "total": "100003.54321", "count": 8}, 
{"date": "2026-03-05", "oil_id": "AST_24", "delivery_type_id": "Street_54", "delivery_basis_id": "st.54", "volume": "10004", "total": "100004.54321", "count": 9}, 
{"date": "2026-03-06", "oil_id": "AST_25", "delivery_type_id": "Street_55", "delivery_basis_id": "st.55", "volume": "10005", "total": "100005.54321", "count": 10}, 
{"date": "2026-03-07", "oil_id": "AST_26", "delivery_type_id": "Street_56", "delivery_basis_id": "st.56", "volume": "10006", "total": "100006.54321", "count": 11}, 
{"date": "2026-03-08", "oil_id": "AST_27", "delivery_type_id": "Street_57", "delivery_basis_id": "st.57", "volume": "10007", "total": "100007.54321", "count": 12}, 
{"date": "2026-03-09", "oil_id": "AST_28", "delivery_type_id": "Street_58", "delivery_basis_id": "st.58", "volume": "10008", "total": "100008.54321", "count": 13}, 
{"date": "2026-03-10", "oil_id": "AST_29", "delivery_type_id": "Street_59", "delivery_basis_id": "st.59", "volume": "10009", "total": "100009.54321", "count": 14}
]
'''
redis_data_dates_5 = '''
[
{"date": "2026-03-01", "oil_id": "AST_20", "delivery_type_id": "Street_50", "delivery_basis_id": "st.50", "volume": "10000", "total": "100000.54321", "count": 5}, 
{"date": "2026-03-02", "oil_id": "AST_21", "delivery_type_id": "Street_51", "delivery_basis_id": "st.51", "volume": "10001", "total": "100001.54321", "count": 6}, 
{"date": "2026-03-03", "oil_id": "AST_22", "delivery_type_id": "Street_52", "delivery_basis_id": "st.52", "volume": "10002", "total": "100002.54321", "count": 7}, 
{"date": "2026-03-04", "oil_id": "AST_23", "delivery_type_id": "Street_53", "delivery_basis_id": "st.53", "volume": "10003", "total": "100003.54321", "count": 8}, 
{"date": "2026-03-05", "oil_id": "AST_24", "delivery_type_id": "Street_54", "delivery_basis_id": "st.54", "volume": "10004", "total": "100004.54321", "count": 9}
]
'''
redis_data_dynamics_5 = '''
[
{"id": "1600de0f-6786-4281-838c-15d65928a8fb", "date": "2026-03-01", "oil_id": "AST_20", "delivery_type_id": "Street_50", "delivery_basis_id": "st.50", "volume": "10000", "total": "100000.54321", "count": 5}, 
{"id": "714b122d-d630-4639-b4f7-7f90b2697b66", "date": "2026-03-02", "oil_id": "AST_21", "delivery_type_id": "Street_51", "delivery_basis_id": "st.51", "volume": "10001", "total": "100001.54321", "count": 6}, 
{"id": "a667d373-2750-4346-a769-b9bb9073bd2f", "date": "2026-03-03", "oil_id": "AST_22", "delivery_type_id": "Street_52", "delivery_basis_id": "st.52", "volume": "10002", "total": "100002.54321", "count": 7}, 
{"id": "d6f7533f-c824-431a-9685-7e5614e69057", "date": "2026-03-04", "oil_id": "AST_23", "delivery_type_id": "Street_53", "delivery_basis_id": "st.53", "volume": "10003", "total": "100003.54321", "count": 8}, 
{"id": "545c3391-a83f-466b-b8ea-18d8b4bed50c", "date": "2026-03-05", "oil_id": "AST_24", "delivery_type_id": "Street_54", "delivery_basis_id": "st.54", "volume": "10004", "total": "100004.54321", "count": 9}
]
'''
redis_data_dynamics_10 = '''
[
{"id": "1600de0f-6786-4281-838c-15d65928a8fb", "date": "2026-03-01", "oil_id": "AST_20", "delivery_type_id": "Street_50", "delivery_basis_id": "st.50", "volume": "10000", "total": "100000.54321", "count": 5}, 
{"id": "714b122d-d630-4639-b4f7-7f90b2697b66", "date": "2026-03-02", "oil_id": "AST_21", "delivery_type_id": "Street_51", "delivery_basis_id": "st.51", "volume": "10001", "total": "100001.54321", "count": 6}, 
{"id": "a667d373-2750-4346-a769-b9bb9073bd2f", "date": "2026-03-03", "oil_id": "AST_22", "delivery_type_id": "Street_52", "delivery_basis_id": "st.52", "volume": "10002", "total": "100002.54321", "count": 7}, 
{"id": "d6f7533f-c824-431a-9685-7e5614e69057", "date": "2026-03-04", "oil_id": "AST_23", "delivery_type_id": "Street_53", "delivery_basis_id": "st.53", "volume": "10003", "total": "100003.54321", "count": 8}, 
{"id": "545c3391-a83f-466b-b8ea-18d8b4bed50c", "date": "2026-03-05", "oil_id": "AST_24", "delivery_type_id": "Street_54", "delivery_basis_id": "st.54", "volume": "10004", "total": "100004.54321", "count": 9}, 
{"id": "f485a4ef-a4f8-41bf-8f36-1763530da4bc", "date": "2026-03-06", "oil_id": "AST_25", "delivery_type_id": "Street_55", "delivery_basis_id": "st.55", "volume": "10005", "total": "100005.54321", "count": 10}, 
{"id": "521ab8c9-0925-4e3c-abf7-2ae4522c6683", "date": "2026-03-07", "oil_id": "AST_26", "delivery_type_id": "Street_56", "delivery_basis_id": "st.56", "volume": "10006", "total": "100006.54321", "count": 11}, 
{"id": "a0bd3a44-2b9f-4003-b0d6-9d7dcf331af4", "date": "2026-03-08", "oil_id": "AST_27", "delivery_type_id": "Street_57", "delivery_basis_id": "st.57", "volume": "10007", "total": "100007.54321", "count": 12}, 
{"id": "8e95d729-4394-4851-93ee-c82fd7fc20cd", "date": "2026-03-09", "oil_id": "AST_28", "delivery_type_id": "Street_58", "delivery_basis_id": "st.58", "volume": "10008", "total": "100008.54321", "count": 13}, 
{"id": "ea1e2f6b-5a0e-41a9-8b16-59554e0e212a", "date": "2026-03-10", "oil_id": "AST_29", "delivery_type_id": "Street_59", "delivery_basis_id": "st.59", "volume": "10009", "total": "100009.54321", "count": 14}
]
'''
redis_data_dynamics_1 = '''
[
{"id": "1600de0f-6786-4281-838c-15d65928a8fb", "date": "2026-03-01", "oil_id": "AST_20", "delivery_type_id": "Street_50", "delivery_basis_id": "st.50", "volume": "10000", "total": "100000.54321", "count": 5}
]
'''


@pytest_asyncio.fixture(scope='session')
async def get_sessionmaker():
    """Единый движок для всех сессий"""

    engine = create_async_engine('sqlite+aiosqlite:///:memory:')

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    session_local = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    yield session_local

    await engine.dispose()


@pytest_asyncio.fixture(scope='function')
async def async_session(get_sessionmaker):
    """Сессия для БД"""

    async with get_sessionmaker() as session:

        yield session

        for table in Base.metadata.sorted_tables:
            await session.execute(table.delete())

        await session.commit()


@pytest_asyncio.fixture(scope='function')
async def create_data(async_session):
    """Создание данных в БД"""

    result = []
    for index in range(10):
        data = {
            'date': date(year=2026, month=3, day=index + 1),
            'oil_id': f'AST_{index + 20}',
            'delivery_type_id': f'Street_{index + 50}',
            'delivery_basis_id': f'st.{index + 50}',
            'volume': Decimal(f'{index + 10_000}'),
            'total': Decimal(f'{index + 100_000.54321}'),
            'count': index + 5
        }

        result.append(SpimexResults(**data))

    async_session.add_all(result)
    await async_session.commit()

    for spimex_obj in result:
        await async_session.refresh(spimex_obj)

    return result


@pytest.fixture(scope='function')
def mock_redis_cache_miss(mocker: MockerFixture):
    """Redis get возвращает None"""

    mock = mocker.AsyncMock()
    mock.get.return_value = None

    return mock


@pytest.fixture(scope='function')
def mock_redis_cache_dates_hit(mocker: MockerFixture):
    """Redis get возвращает не None dates"""

    mock = mocker.AsyncMock()
    redis_key = 'trading:dates:last_days'

    def dynamic_effect(key: str):
        """Динамичное возвращение значение мока"""

        if key == f'{redis_key}:30':
            return redis_data_dates_10
        elif key == f'{redis_key}:20':
            return redis_data_dates_10
        elif key == f'{redis_key}:5':
            return redis_data_dates_5
        return None

    mock.get.side_effect = dynamic_effect

    return mock


@pytest_asyncio.fixture(scope='function')
async def mock_redis_cache_dynamics_hit(mocker: MockerFixture):
    """Redis get возвращает не None dynamics"""
    params = [
        {
            'start_date': date(year=2026, month=3, day=1),
            'end_date': date(year=2026, month=3, day=5),
            'oil_id': None,
            'delivery_type_id': None,
            'delivery_basis_id': None
        },
        {
            'start_date': date(year=2026, month=3, day=1),
            'end_date': date(year=2026, month=3, day=10),
            'oil_id': None,
            'delivery_type_id': None,
            'delivery_basis_id': None
        },
        {
            'start_date': date(year=2026, month=3, day=1),
            'end_date': date(year=2026, month=3, day=5),
            'oil_id': 'AST_20',
            'delivery_type_id': 'Street_50',
            'delivery_basis_id': 'st.50'
        },
        {
            'start_date': date(year=2026, month=3, day=1),
            'end_date': date(year=2026, month=3, day=1),
            'oil_id': 'AST_21',
            'delivery_type_id': 'Street_55',
            'delivery_basis_id': 'st.60'
        }
    ]

    mock = mocker.AsyncMock()
    hash_params = [await get_hash_params_dynamics(**param) for param in params]
    cache_name = 'trading:dynamics'

    def dynamic_effect(key: str):
        if key == f'{cache_name}:{hash_params[0]}':
            return redis_data_dynamics_5
        elif key == f'{cache_name}:{hash_params[1]}':
            return redis_data_dynamics_10
        elif key == f'{cache_name}:{hash_params[2]}':
            return redis_data_dynamics_1
        elif key == f'{cache_name}:{hash_params[3]}':
            return '[]'
        return None

    mock.get.side_effect = dynamic_effect

    return mock


@pytest.fixture(scope='function', autouse=True)
def mock_app_settings(mocker: MockerFixture):
    """Заглушка для некоторых надстроек"""

    mocker.patch('core.settings.Settings.initialize_redis')
    mocker.patch('core.settings.Settings.close_redis_connect')

import pytest
import pytest_asyncio

from pytest_mock import MockerFixture

from datetime import date
from decimal import Decimal

from fastapi.testclient import TestClient

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from database.core import Base, get_connection
from database.models import SpimexResults
from core import get_redis
from main import app


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

        await session.rollback()


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
def mock_redis_cache_hit(mocker: MockerFixture):
    """Redis get возвращает не None"""

    mock = mocker.AsyncMock()
    mock.get.return_value = '''
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
    {"date": "2026-03-10", "oil_id": "AST_29", "delivery_type_id": "Street_59", "delivery_basis_id": "st.59", "volume": "10009", "total": "100009.54321", "count": 14}]
    '''

    return mock


@pytest.fixture(scope='function', autouse=True)
def mock_app_settings(mocker: MockerFixture):
    """Заглушка для некоторых надстроек"""

    mocker.patch('core.settings.Settings.initialize_redis')
    mocker.patch('core.settings.Settings.close_redis_connect')


@pytest.fixture(scope='function')
def client_test_cache_miss(mock_redis_cache_miss, async_session):
    """Переопределение зависимостей get_connection и async_redis при cache miss"""

    app.dependency_overrides[get_connection] = lambda: async_session
    app.dependency_overrides[get_redis] = lambda: mock_redis_cache_miss

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture(scope='function')
def client_test_cache_hit(mock_redis_cache_hit, async_session):
    """Переопределение зависимостей get_connection и async_redis при cache hit"""

    app.dependency_overrides[get_connection] = lambda: async_session
    app.dependency_overrides[get_redis] = lambda: mock_redis_cache_hit

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()

import pytest

from fastapi.testclient import TestClient

from main import app


health_url = '/api/v1/routers/test/ping'


@pytest.mark.integration
def test_check_health_url():
    """Тестирование работоспособности"""

    with TestClient(app) as client:
        response = client.get(health_url)

    assert response.status_code == 200
    assert response.json() == {'message': 'pong'}

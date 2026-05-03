import pytest

from fastapi.testclient import TestClient

from main import app


url = '/api/v1/routers/test/ping'


@pytest.mark.integration
def test_check_health_url():
    """Тестирование работоспособности"""

    with TestClient(app) as client:
        response = client.get(url)

    assert response.status_code == 200
    assert response.json() == {'message': 'pong'}

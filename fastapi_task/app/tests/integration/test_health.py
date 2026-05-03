import pytest

from fastapi.testclient import TestClient

from main import app


@pytest.mark.integration
def test_check_health_url():
    """Тестирование работоспособности"""

    with TestClient(app) as client:
        response = client.get('/api/v1/routers/test/ping')

    assert response.status_code == 200
    assert response.json() == {'message': 'pong'}

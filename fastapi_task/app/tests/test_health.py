import asyncio
import httpx


base_url = '/api/v1/routers/test/ping'


async def test_health_service(client: httpx.AsyncClient) -> None:
    """Тестирование /api/v1/routers/test/ping"""

    response = await client.get(base_url)

    assert response.status_code == 200
    assert response.json() == {'message': 'pong'}


async def test_health_service_broken(client: httpx.AsyncClient) -> None:
    """Тестирование различных методов"""

    responses = await asyncio.gather(*[client.post(base_url), client.patch(base_url), client.put(base_url), client.delete(base_url)])
    responses_status = [response.status_code for response in responses]
    responses_data = [response.json() for response in responses]

    assert responses_status == [405, 405, 405, 405]
    assert responses_data == [{'detail': 'Method Not Allowed'} for _ in range(4)]

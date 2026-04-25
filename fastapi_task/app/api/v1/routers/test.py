from fastapi import APIRouter


test_router = APIRouter(
    prefix='/api/v1/routers/test',
    tags=['Для теста', ]
)


@test_router.get(
    '/ping',
    summary='Тестирование работоспособности',
    description='Возвращает "pong" при обращении',
)
async def pong() -> dict:
    return {'message': 'pong'}

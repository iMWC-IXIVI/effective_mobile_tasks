from fastapi import FastAPI, APIRouter


def include_routers(app: FastAPI, routers: list[APIRouter]) -> None:
    """Подключение роутеров"""

    for router in routers:
        app.include_router(router)

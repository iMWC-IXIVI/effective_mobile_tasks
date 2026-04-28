from fastapi import FastAPI

from prometheus_fastapi_instrumentator import Instrumentator

from core import lifespan
from utils import include_routers
from api.v1 import test_router, trading_router


app = FastAPI(
    title='Микросервис для торговых данных',
    version='0.0.1',
    description='Получение данных из сайта SPIMEX',
    lifespan=lifespan
)

routers = [test_router, trading_router]
include_routers(app, routers)

instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

from fastapi import FastAPI

from utils import include_routers
from api.v1 import test_router


app = FastAPI(
    title='Микросервис для торговых данных',
    version='0.0.1',
    description='Получение данных из сайта SPIMEX'
)

routers = [test_router, ]
include_routers(app, routers)

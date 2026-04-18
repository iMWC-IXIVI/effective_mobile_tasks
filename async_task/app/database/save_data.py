from parser.model_validate import ValidateData

from .core import AsyncSessionLocal
from .models import Spimex


async def save_data(datas: list[ValidateData]) -> None:
    """Сохранение данных в БД"""

    async with AsyncSessionLocal() as session:
        async with session.begin():
            session.add_all([Spimex(**data.model_dump()) for data in datas])

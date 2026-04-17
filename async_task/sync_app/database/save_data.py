# from parser.model_validate import ValidateData TODO list[ValidateData]

from .core import SessionLocal
from .models import Spimex


def save_data(datas: list) -> None:
    """Сохранение данных в БД"""

    with SessionLocal() as session:
        with session.begin():
            session.add_all([Spimex(**data.model_dump()) for data in datas])

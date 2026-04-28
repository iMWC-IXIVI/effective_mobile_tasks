from datetime import date

from pydantic import BaseModel


class DateSchema(BaseModel):
    """Схема для возвращения даты"""

    date: date

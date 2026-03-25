from enum import StrEnum
from datetime import date

from sqlalchemy import Integer, String, Date, Enum
from sqlalchemy.orm import Mapped, mapped_column

from core import Base


class CountryCode(StrEnum):
    RU = 'RU'
    US = 'US'


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, comment='Идентификатор')
    username: Mapped[str] = mapped_column(String(50), comment='Имя')
    email: Mapped[str] = mapped_column(String(100), comment='Электронная почта')
    country_code: Mapped[CountryCode] = mapped_column(Enum(CountryCode), comment='Код страны')
    registration_date: Mapped[date] = mapped_column(Date(), default=date.today, server_default='CURRENT_DATE', comment='Дата регистрации')
    rating: Mapped[int] = mapped_column(Integer, default=0, server_default='0', comment='Рейтинг')

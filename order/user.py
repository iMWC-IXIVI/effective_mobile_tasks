import uuid

from abc import ABC, abstractmethod
from typing import Any

from datetime import date

from exceptions import UserValueError
from discount import LoyaltyDiscount, SpecDiscount


class User(ABC):
    """
    Класс содержит информацию о пользователе

    :param name: str (имя для пользователя)
    :param date_of_birth (дата рождения, возможность дать спец предложение во время дня рождения)

    Атрибуты:
    id: UUID (идентификатор пользователя)
    pur_counter: int (счётчик покупок)
    discount: list[LoyaltyDiscount | SpecDiscount] (тип скидки для пользователя, могут быть несколько)
    """
    def __init__(self, name: str, date_of_birth: date) -> None:
        if not name or not isinstance(name, str):
            raise UserValueError('Поле name должно быть не пустым или принадлежать str')

        if not date_of_birth or not isinstance(date_of_birth, date):
            raise UserValueError('Поле date_of_birth должно быть не пустым или принадлежать date')

        self.name = name
        self.date_of_birth = date_of_birth

        self.id = uuid.uuid4()
        self.pur_counter: int = 0
        self.discount: list[LoyaltyDiscount | SpecDiscount] | None = None

    @abstractmethod
    def added_discount_for_loyalty(self) -> None:
        """Метод для получения LoyaltyDiscount, для постоянного покупателя за счет self.pur_counter"""

    @abstractmethod
    def added_discount_for_spec(self) -> None:
        """Метод для получения SpecDiscount, в качестве дня рождения"""

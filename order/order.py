import uuid

from abc import ABC, abstractmethod
from typing import Any

from exceptions import OrderValueError
from discount import FixedDiscount, PercentDiscount
from user import User


class Order(ABC):
    """
    Класс содержит информацию о заказе

    :param user: User (имя пользователя)
    :param price: int (цена заказа)
    :param discount: Any[FixedDiscount, PercentDiscount] | None = None (скидка на товар если она есть)

    Атрибуты:
    id: uuid.UUID (идентификатор заказа)
    """
    def __init__(self, user: User, price: int, discount: Any[FixedDiscount, PercentDiscount] | None = None) -> None:
        if not user or not isinstance(user, User):
            raise OrderValueError('Поле user должен быть не пустым или принадлежать типу User')

        if not price or not isinstance(price, int):
            raise OrderValueError('Поле price должен быть не пустым или принадлежать типу int')

        self.user = user
        self.price = None
        self.discount = discount
        self.id: uuid.UUID = uuid.uuid4()

    @staticmethod
    @abstractmethod
    def user_discount(user: User):
        """Подсчет скидки принадлежащий у пользователя"""

    @abstractmethod
    def price_with_discounts(self):
        """Подсчёт скидки с учетом на сам заказ + скидка у пользователя"""

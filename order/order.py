import uuid

from abc import ABC, abstractmethod
from typing import Any

from exceptions import OrderValueError
from discount import FixedDiscount, PercentDiscount
from user import User


class BaseOrder(ABC):
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
        self.price = price
        self.discount = discount
        self.id: uuid.UUID = uuid.uuid4()

    @staticmethod
    @abstractmethod
    def user_discount(user: User) -> int | float:
        """Подсчет скидки принадлежащий у пользователя"""
        pass

    @abstractmethod
    def price_with_discounts(self) -> int:
        """Пересчёт суммы заказа"""
        pass


class Order(BaseOrder):
    @staticmethod
    def user_discount(user: User) -> int | float:
        user_discount = 0
        if user.discount:
            for dis in user.discount:
                user_discount += dis.value
                dis.activate()
        return user_discount

    def price_with_discounts(self) -> int:
        if self.discount:
            self.discount.activate()

        final_price = self.price
        user_discount = self.user_discount(self.user)

        if user_discount:
            final_price = final_price * (1 - user_discount / 100)

        if self.discount:
            if isinstance(self.discount, FixedDiscount):
                final_price -= self.discount.value
            elif isinstance(self.discount, PercentDiscount):
                final_price = final_price * (1 - self.discount.value / 100)

        self.price = int(max(0, final_price))

        return self.price

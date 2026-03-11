from dataclasses import dataclass
from decimal import Decimal
from typing import Callable
from functools import wraps

from currency import Currency
from exceptions import WalletDoesNotFound, WalletLTZero


def check_data(func: Callable):
    @wraps(func)
    def wrapper(self, currency: Currency, value: Decimal, *args, **kwargs):
        if self.currency.get(currency) is None:
            raise WalletDoesNotFound('Ваш кошелёк не поддерживает данную валюту')

        if not isinstance(value, Decimal):
            raise TypeError('Цена должна быть в Decimal')

        if value <= 0:
            raise ValueError('Цена должна быть больше 0')

        func(self, currency, value)
    return wrapper


@dataclass
class Wallet:
    currency: list[Currency]

    def __post_init__(self):
        self.currency: dict[Currency, Decimal] = {k: Decimal(0) for k in self.currency}

    @check_data
    def replenishment(self, currency: Currency, value: Decimal) -> None:
        self.currency[currency] += value

    @check_data
    def withdraw(self, currency: Currency, value: Decimal) -> None:
        if self.currency[currency] - value < 0:
            raise WalletLTZero('Баланс не может быть меньше 0')

        self.currency[currency] -= value

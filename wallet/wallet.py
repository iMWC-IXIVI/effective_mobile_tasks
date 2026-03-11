from dataclasses import dataclass
from decimal import Decimal

from currency import Currency
from exceptions import WalletDoesNotFound, WalletLTZero


@dataclass
class Wallet:
    currency: list[Currency]

    def __post_init__(self):
        self.currency: dict[Currency, Decimal] = {k: Decimal(0) for k in self.currency}

    def replenishment(self, currency: Currency, value: Decimal) -> None:
        if self.currency.get(currency) is None:
            raise WalletDoesNotFound('Ваш кошелёк не поддерживает данную валюту')

        if not isinstance(value, Decimal):
            raise TypeError('Цена должна быть в Decimal')

        if value <= 0:
            raise ValueError('Цена должна быть больше 0')

        self.currency[currency] += value

    def withdraw(self, currency: Currency, value: Decimal) -> None:
        if self.currency.get(currency) is None:
            raise WalletDoesNotFound('Ваш кошелёк не поддерживает данную валюту')

        if not isinstance(value, Decimal):
            raise TypeError('Цена должна быть в Decimal')

        if value <= 0:
            raise ValueError('Цена должна быть больше 0')

        if self.currency[currency] - value < 0:
            raise WalletLTZero('Баланс не может быть меньше 0')

        self.currency[currency] -= value

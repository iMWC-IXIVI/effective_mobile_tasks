import enum

from abc import ABC, abstractmethod

from exceptions import DiscountValueError


class EnumDiscount(enum.Enum):
    FIXED = enum.auto()
    LOYALTY = enum.auto()
    SPEC = enum.auto()
    PERCENT = enum.auto()


class Discount(ABC):
    """
    Базовый класс скидок

    :param name: EnumDiscount (название скидки)
    :param value: int | float (скидка)

    Атрибуты:
    is_active: bool (Активна ли скидка)
    """
    def __init__(self, name: EnumDiscount, value: float | int) -> None:
        if not name or not isinstance(name, EnumDiscount):
            raise DiscountValueError('Поле name должно быть не пустым или принадлежать EnumDiscount')

        if not value or not isinstance(value, int | float):
            raise DiscountValueError('Поле value должно быть не пустым или принадлежать int или float')

        self.name = name
        self.value = value

        self.is_active: bool = False

    @abstractmethod
    def activate(self) -> None:
        """Активация скидки"""

    @abstractmethod
    def deactivate(self) -> None:
        """Деактивация скидки"""


class FixedDiscount(Discount):
    def __init__(self, value: int | float) -> None:
        super().__init__(name=EnumDiscount.FIXED, value=value)

    def activate(self) -> None: pass
    def deactivate(self) -> None: pass


class LoyaltyDiscount(Discount):
    def __init__(self, value: int | float) -> None:
        super().__init__(name=EnumDiscount.LOYALTY, value=value)

    def activate(self) -> None: pass
    def deactivate(self) -> None: pass


class SpecDiscount(Discount):
    def __init__(self, value: int | float) -> None:
        super().__init__(name=EnumDiscount.SPEC, value=value)

    def activate(self) -> None: pass
    def deactivate(self) -> None: pass


class PercentDiscount(Discount):
    def __init__(self, value: int | float) -> None:
        super().__init__(name=EnumDiscount.PERCENT, value=value)

    def activate(self) -> None: pass
    def deactivate(self) -> None: pass

import uuid

from typing import Optional
from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UUID, String, DECIMAL, Integer

from .core import Base


class Spimex(Base):
    """Таблица в БД"""

    __tablename__ = 'spimex'

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4, comment='Идентификатор')
    code_item: Mapped[str] = mapped_column(String(20), unique=True, comment='Код инструмента')
    name_item: Mapped[str] = mapped_column(String(255), comment='Наименование инструмента')
    basis_delivery: Mapped[str] = mapped_column(String(255), comment='Базис поставки')
    volume: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(10, 2), comment='Объем договоров в единицах измерения')
    volume_rub: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(10, 2), comment='Объем договоров, руб.')
    price_change_run: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(10, 2), comment='Изменение цены к цене предыдущего дня (руб.)')
    price_change_percent: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(10, 2), comment='Изменение цены к цене предыдущего дня (%)')
    minimum_price: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(10, 2), comment='Минимальная цена')
    avg_price: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(10, 2), comment='Средневзвешенная цена')
    maximum_price: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(10, 2), comment='Максимальная цена')
    market_price: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(10, 2), comment='Рыночная цена')
    best_price: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(10, 2), comment='Цена заявки (Лучшее предложение)')
    best_demand: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(10, 2), comment='Цена заявки (Лучший спрос)')
    counter: Mapped[Optional[int]] = mapped_column(Integer, comment='Количество сделок шт.')

    def __repr__(self):
        return f'{self.__class__.__name__}({self.code_item})'

    def __str__(self):
        return f'{self.code_item}-{self.name_item}'

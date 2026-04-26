import uuid

from datetime import date
from decimal import Decimal
from typing import Optional

from sqlalchemy import UUID, Date, String, DECIMAL, Integer
from sqlalchemy.orm import Mapped, mapped_column, validates

from database.core import Base


class SpimexResults(Base):
    """Таблица для сохранения результатов торгов"""

    __tablename__ = 'spimex_trading_results'

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4, comment='Уникальный идентификатор UUID')
    date: Mapped[date] = mapped_column(Date, default=date.today(), index=True, comment='Дата торгов')
    oil_id: Mapped[str] = mapped_column(String(50), index=True, comment='Идентификатор нефтяного продукта')
    delivery_type_id: Mapped[str] = mapped_column(String(255), index=True, comment='Тип поставки')
    delivery_basis_id: Mapped[str] = mapped_column(String(255), index=True, comment='Базис поставки')
    volume: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(18, 6), comment='Объем торгов')
    total: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(18, 6), comment='Общая сумма')
    count: Mapped[Optional[int]] = mapped_column(Integer, comment='Количество сделок')

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(uuid={self.id})'

    def __str__(self) -> str:
        return f'id={self.id}, oil_id={self.oil_id}'

    @validates('count')
    def validate_count(self, _, value: Optional[int]) -> Optional[int]:
        """Валидация поля count на отрицательное число"""

        if value is not None:
            if value < 0:
                raise ValueError('Значение "количества сделок" не может быть меньше нуля')
        return value

    def to_dict(self) -> dict:
        """Возвращение dict экземпляра"""
        return {
            'id': self.id,
            'date': self.date,
            'oil_id': self.oil_id,
            'delivery_type_id': self.delivery_type_id,
            'delivery_basis_id': self.delivery_basis_id,
            'volume': self.volume,
            'total': self.total,
            'count': self.count
        }

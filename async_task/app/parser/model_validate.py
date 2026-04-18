from decimal import Decimal

from typing import Optional, Any

from pydantic import BaseModel, Field, ConfigDict, field_validator


class ValidateData(BaseModel):
    """Модель для валидации данных"""

    code_item: str = Field(alias='Код инструмента')
    name_item: str = Field(alias='Наименование инструмента')
    basis_delivery: str = Field(alias='Базис поставки')
    volume: Optional[Decimal] = Field(alias='Объем договоров в единицах измерения')
    volume_rub: Optional[Decimal] = Field(alias='Объем договоров, руб.')
    price_change_rub: Optional[Decimal] = Field(alias='Изменение цены к цене предыдущего дня (руб.)')
    price_change_percent: Optional[Decimal] = Field(alias='Изменение цены к цене предыдущего дня (%)')
    minimum_price: Optional[Decimal] = Field(alias='Минимальная цена')
    avg_price: Optional[Decimal] = Field(alias='Средневзвешенная цена')
    maximum_price: Optional[Decimal] = Field(alias='Максимальная цена')
    market_price: Optional[Decimal] = Field(alias='Рыночная цена')
    best_price: Optional[Decimal] = Field(alias='Цена заявки (Лучшее предложение)')
    best_demand: Optional[Decimal] = Field(alias='Цена заявки (Лучший спрос)')
    counter: Optional[int] = Field(alias='Количество сделок шт.')

    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True
    )

    @field_validator('volume', 'volume_rub', 'price_change_rub', 'price_change_percent', 'minimum_price', 'avg_price', 'maximum_price', 'market_price', 'best_price', 'best_demand', mode='before')
    @classmethod
    def valid_decimal(cls, value: Any) -> Optional[Decimal]:
        """Валидация полей с типом данных Optional[Decimal]"""

        if isinstance(value, str) and value == '-':
            return None

        if isinstance(value, str):
            value = value.replace(',', '.').replace(' ', '')

        return Decimal(value)

    @field_validator('counter', mode='before')
    @classmethod
    def valid_integer(cls, value) -> Optional[int]:
        """Валидация поля с типом данных Optional[int]"""

        if isinstance(value, str) and value == '-':
            return None

        return int(value)

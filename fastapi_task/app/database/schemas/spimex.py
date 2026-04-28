import uuid

from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class SpimexSchema(BaseModel):
    """Схема для возвращения данных из бд SpimexResults"""

    id: uuid.UUID
    date: date
    oil_id: str
    delivery_type_id: str
    delivery_basis_id: str
    volume: Decimal | None = None
    total: Decimal | None = None
    count: int | None = None

    model_config = ConfigDict(from_attributes=True)

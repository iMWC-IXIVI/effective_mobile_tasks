from datetime import date, datetime

from sqlalchemy import Integer, String, Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from core import Base


class SpimexTradingResult(Base):
    __tablename__ = 'spimex_trading_results'

    id: Mapped[int] = mapped_column(primary_key=True)
    exchange_product_id: Mapped[str | None] = mapped_column(String(50))
    exchange_product_name: Mapped[str] = mapped_column(String(255))
    oil_id: Mapped[str] = mapped_column(String(4))
    delivery_basis_id: Mapped[str] = mapped_column(String(4))
    delivery_basis_name: Mapped[str] = mapped_column(String(1))
    delivery_type_id: Mapped[str] = mapped_column(String(1))
    volume: Mapped[int | None] = mapped_column(Integer())
    total: Mapped[int] = mapped_column(Integer())
    count: Mapped[int] = mapped_column(Integer())
    date: Mapped[date] = mapped_column(Date())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=datetime.now)

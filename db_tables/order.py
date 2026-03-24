from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core import Base


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True, comment='Идентификатор')
    message: Mapped[str] = mapped_column(String, comment='Пожелания')

    client_id: Mapped[int] = mapped_column(ForeignKey('Client.id', ondelete='CASCADE'))
    client = relationship('Client', back_populates='orders')

    book_orders = relationship('OrderBook', back_populates='order', cascade='all, delete-orphan', passive_deletes=True)

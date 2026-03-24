from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


from core import Base


class OrderBook(Base):
    __tablename__ = 'book_orders'

    id: Mapped[int] = mapped_column(primary_key=True, comment='Идентификатор')
    counter: Mapped[int] = mapped_column(Integer, comment='Количество заказов')

    book_id: Mapped[int] = mapped_column(ForeignKey('Book.id', ondelete='CASCADE'))
    book = relationship('Book', back_populates='book_orders')

    order_id: Mapped[int] = mapped_column(ForeignKey('Order.id', ondelete='CASCADE'))
    order = relationship('Order', back_populates='book_orders')

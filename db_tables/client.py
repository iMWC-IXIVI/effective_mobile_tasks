from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


from core import Base


class Client(Base):
    __tablename__ = 'clients'

    id: Mapped[int] = mapped_column(primary_key=True, comment='Идентификатор')
    name: Mapped[str] = mapped_column(String(255), index=True, comment='Имя')
    email: Mapped[str] = mapped_column(String(255), comment='Почта')

    city_id: Mapped[int] = mapped_column(ForeignKey('City.id', ondelete='CASCADE'))
    city = relationship('City', back_populates='clients')

    orders = relationship('Order', back_populates='client', cascade='all, delete-orphan', passive_deletes=True)

    order_steps = relationship('OrderStep', back_populates='client', cascade='all, delete-orphan', passive_deletes=True)

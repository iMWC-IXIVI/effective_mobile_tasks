from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core import Base


class OrderStep(Base):
    __tablename__ = 'order_steps'

    id: Mapped[int] = mapped_column(primary_key=True)
    start_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    client_id: Mapped[int] = mapped_column(ForeignKey('clients.id', ondelete='CASCADE'))
    client = relationship('Client', back_populates='order_steps')

    step_id: Mapped[int] = mapped_column(ForeignKey('steps.id', ondelete='CASCADE'))
    step = relationship('Step', 'order_steps')

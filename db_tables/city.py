from datetime import time

from sqlalchemy import String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core import Base


class City(Base):
    __tablename__ = 'cities'

    id: Mapped[int] = mapped_column(primary_key=True, comment='Идентификатор')
    name: Mapped[str] = mapped_column(String(100), index=True, comment='Название')
    delivery_time: Mapped[time] = mapped_column(Time(timezone=True))

    clients = relationship('Client', back_populates='city', cascade='all, delete-orphan', passive_deletes=True)

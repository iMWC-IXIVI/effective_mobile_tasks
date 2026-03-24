from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core import Base


class Step(Base):
    __tablename__ = 'steps'

    id: Mapped[int] = mapped_column(primary_key=True)
    steps: Mapped[str] = mapped_column(String())

    order_steps = relationship('OrderStep', back_populates='step', cascade='all, delete-orphan', passive_deletes=True)

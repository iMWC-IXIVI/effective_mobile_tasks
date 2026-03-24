from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core import Base


class Author(Base):
    __tablename__ = 'authors'

    id: Mapped[int] = mapped_column(primary_key=True, comment='Идентификатор')
    name: Mapped[str] = mapped_column(String(100), index=True, comment='Имя')

    books = relationship('Book', back_populates='author', cascade='all, delete-orphan', passive_deletes=True)

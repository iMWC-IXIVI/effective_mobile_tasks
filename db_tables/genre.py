from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core import Base


class Genre(Base):
    __tablename__ = 'genres'

    id: Mapped[int] = mapped_column(primary_key=True, comment='Идентификатор')
    name: Mapped[str] = mapped_column(String(255), index=True, comment='Название жанра')

    books = relationship('Book', back_populates='genre', cascade='all, delete-orphan', passive_deletes=True)

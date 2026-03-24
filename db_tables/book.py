from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from core import Base


class Book(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True, comment='Идентификатор')
    name: Mapped[str] = mapped_column(String(255), index=True, comment='Название')
    price: Mapped[int] = mapped_column(Integer, comment='Цена')
    counter: Mapped[int] = mapped_column(Integer, comment='Количество на складе')

    genre_id: Mapped[int] = mapped_column(ForeignKey('Genre.id', ondelete='CASCADE'))
    genre = relationship('Genre', back_populates='books')

    author_id: Mapped[int] = mapped_column(ForeignKey('Author.id', ondelete='CASCADE'))
    author = relationship('Author', back_populates='books')

from core import Base, engine

from db_tables.author import Author
from db_tables.book import Book
from db_tables.city import City
from db_tables.client import Client
from db_tables.genre import Genre
from db_tables.order import Order
from db_tables.order_book import OrderBook
from db_tables.order_step import OrderStep
from db_tables.step import Step


def create_tables() -> None:
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    create_tables()

from core import Base, engine

from spimex_table import SpimexTradingResult


def create_all_tables():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    create_all_tables()

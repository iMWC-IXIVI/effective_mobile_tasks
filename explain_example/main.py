import random

from core import Base, Session, engine
from user import User, CountryCode


country_code = list(CountryCode)


def create_all_tables():
    """Создание таблиц"""
    Base.metadata.create_all(engine)


def data():
    """Генерация данных для дб"""
    for i in range(1_000_000):
        yield {
            'username': f'User({i})',
            'email': f'example_user_{i}@ex.me',
            'country_code': random.choice(country_code)
        }


def insert_data() -> None:
    """Создание миллиона записей в бд"""
    with Session() as session:
        session.bulk_insert_mappings(User, data())
        session.commit()


if __name__ == '__main__':
    # Создание таблицы users
    # create_all_tables()

    # Создание миллиона записей в бд
    # insert_data()
    pass

import random

from functools import wraps
from time import perf_counter

from sqlalchemy.future import select
from sqlalchemy import text

from core import Base, Session, engine
from user import User, CountryCode


country_code = list(CountryCode)


def timer(func):
    """Декоратор для измерения времени"""
    @wraps(func)
    def wrapper(*args, **kwargs):

        start = perf_counter()
        result = func(*args, **kwargs)
        end = perf_counter()

        print(f'Func - {func.__name__}\nResult - {result}\nTimer -{end - start: .4f}s')

        return result, end - start
    return wrapper


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


@timer
def explain_analyze_data():
    """Выполнение указанного запроса"""
    query = select(User).where(User.country_code == CountryCode.RU, User.rating < 100)
    compiled = query.compile(
        compile_kwargs={'literal_binds': True}
    )

    with Session() as session:
        db_result = session.execute(text(f'EXPLAIN ANALYZE {compiled}'))
        result = db_result.scalars().all()

    return result


if __name__ == '__main__':
    # Создание таблицы users
    # create_all_tables()

    # Создание миллиона записей в бд
    # insert_data()

    # Задание №1. Выполните следующий запрос и с помощью EXPLAIN ANALYZE замерьте его время выполнения и стоимость
    # SELECT * FROM users WHERE country_code = 'RU' AND rating > 100
    # ['Seq Scan on users  (cost=0.00..25310.00 rows=499167 width=53) (actual time=0.006..66.055 rows=498833 loops=1)', "  Filter: ((rating < 100) AND (country_code = 'RU'::countrycode))", '  Rows Removed by Filter: 501167', 'Planning Time: 0.049 ms', 'Execution Time: 76.335 ms']
    # Get data = 0.0838s
    # ==============ДАЛЬШЕ КОД===============
    # total_counter = 0
    # for _ in range(10):
    #     total_counter += explain_analyze_data()[1]
    # print(f'Get data = {total_counter / 10:.4f}s')

    pass
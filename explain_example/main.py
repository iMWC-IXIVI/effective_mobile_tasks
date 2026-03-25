import random

from functools import wraps
from time import perf_counter

from sqlalchemy.future import select
from sqlalchemy import text, Index

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


@timer
def add_index_country_code() -> None:
    """Добавление индекса по полю country_code"""
    Index('idx_users_country_code', User.country_code).create(bind=engine, checkfirst=True)


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

    # Задание №2. Создайте индекс, который, по вашему мнению, максимально ускорит этот запрос. Объясните, почему вы выбрали именно такой тип/комбинацию полей.
    # Сначала добавляю индекс для равенства, а потом для сравнения, важно, что не все индексы стоит добавлять, поэтому, сначала добавлю по полю countre_code, если записей будет много, то стоит добавить и по rating
    # add_index_country_code()

    # Задание №3. Снова выполните EXPLAIN ANALYZE для того же запроса. Сравните показатели cost, время и использованный план (Seq Scan vs Index Scan).
    # ['Bitmap Heap Scan on users  (cost=5564.97..23362.47 rows=499167 width=53) (actual time=9.058..55.054 rows=498833 loops=1)', "  Recheck Cond: (country_code = 'RU'::countrycode)", '  Filter: (rating < 100)', '  Heap Blocks: exact=10310', '  ->  Bitmap Index Scan on idx_users_country_code  (cost=0.00..5440.18 rows=499167 width=0) (actual time=8.169..8.169 rows=498833 loops=1)', "        Index Cond: (country_code = 'RU'::countrycode)", 'Planning Time: 0.070 ms', 'Execution Time: 65.020 ms']
    # Get data = 0.0720s
    # ==============ДАЛЬШЕ КОД===============
    # total_counter = 0
    # for _ in range(10):
    #     total_counter += explain_analyze_data()[1]
    # print(f'Get data = {total_counter / 10:.4f}s')

    # Задание №4. Вопрос для размышления: Почему простого индекса на country_code может быть недостаточно? Что происходит с данными после фильтрации по стране?
    # В случае с моим примером, у меня результат по country_code равняется примерно 500_000, это слишком много, и в нынешней реализации SQL снова придётся перебирать записи из 500_000 и искать уже по rating где rating < 100
    # Стоит в функцию add_index_country_code() добавить ещё и rating и переименовать непосредственно название функции и название самого индекса.
    pass

from time import perf_counter
from datetime import datetime
from typing import Generator

from sqlalchemy.future import select
from sqlalchemy import func

from core import Base, engine, URL, SRC_PATH, Session
from parser import main as parser_main
from parse_data import read_table_pdf, parse_pdf, get_table_xls, parse_xls

from spimex_table import SpimexTradingResult


def create_all_tables():
    Base.metadata.create_all(bind=engine)


def save_from_xls(list_files: Generator) -> None:
    for excel_file in list_files:
        date_file = datetime.strptime(excel_file.stem, '%d.%m.%Y').date()

        query = select(SpimexTradingResult.date).filter_by(date=date_file)

        with Session() as session:
            result = session.execute(query).first()

        if result:
            continue

        table = get_table_xls(excel_file)
        datas = parse_xls(table, date_file)

        with Session() as session:
            session.bulk_insert_mappings(SpimexTradingResult, datas)


def save_from_pdf(list_files: Generator) -> None:
    for pdf_file in list_files:
        date_file = datetime.strptime(pdf_file.stem, '%d.%m.%Y').date()

        query = select(SpimexTradingResult.date).filter_by(date=date_file)

        with Session() as session:
            result = session.execute(query).first()
            session.commit()

        if result:
            continue

        table = read_table_pdf(pdf_file)
        datas = parse_pdf(table, date_file)

        with Session() as session:
            session.bulk_insert_mappings(SpimexTradingResult, datas)
            session.commit()


def get_count_rows() -> int:
    query = select(func.count()).select_from(SpimexTradingResult)

    with Session() as session:
        result = session.execute(query).scalar()

    return result


def main():
    timer = perf_counter()

    start_timer_parser = perf_counter()
    parser_main(URL)
    end_timer_parser = perf_counter()

    excels_files = SRC_PATH.glob('*.xls')
    pdf_files = SRC_PATH.glob('*.pdf')

    start_timer_save_xls = perf_counter()
    save_from_xls(excels_files)
    end_timer_save_xls = perf_counter()

    start_timer_save_pdf = perf_counter()
    save_from_pdf(pdf_files)
    end_timer_save_pdf = perf_counter()

    end_timer = perf_counter()

    print(f'Время загрузки файлов - {end_timer_parser - start_timer_parser}s\n'
          f'Время сохранения данных в БД из файлов xls - {end_timer_save_xls - start_timer_save_xls}s\n'
          f'Время сохранения данных в БД из файлов pdf - {end_timer_save_pdf - start_timer_save_pdf}s\n'
          f'Время выполнения программы - {end_timer - timer}s\n'
          f'Количество записей в БД - {get_count_rows()}')


if __name__ == '__main__':
    create_all_tables()
    main()


"""
Время загрузки файлов - 145.30304500000784s
Время сохранения данных в БД из файлов xls - 84.71288570000615s
Время сохранения данных в БД из файлов pdf - 372.1940612999897s
Время выполнения программы - 602.2099976000027s
Количество записей в БД - 15299
"""
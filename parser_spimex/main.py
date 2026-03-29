from datetime import datetime
from typing import Generator

from sqlalchemy.future import select

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


def main():
    parser_main(URL)

    excels_files = SRC_PATH.glob('*.xls')
    pdf_files = SRC_PATH.glob('*.pdf')

    save_from_xls(excels_files)
    save_from_pdf(pdf_files)


if __name__ == '__main__':
    create_all_tables()
    main()

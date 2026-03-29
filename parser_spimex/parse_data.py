import pdfplumber
import pandas as pd

from datetime import datetime
from typing import Generator


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


pdf_fields = {
    'exchange_product_id': 0,
    'exchange_product_name': 1,
    'volume': 3,
    'total': 4,
    'count': -1
}

excel_fields = {
    0: 'Код инструмента',
    1: 'Наименование инструмента',
    2: 'Базис поставки',
    3: 'Объем договоров в единицах измерения',
    4: 'Объем договоров, руб.',
    5: 'Изменение рыночной цены к цене предыдущего дня в руб.',
    6: 'Изменение рыночной цены к цене предыдущего дня в %',
    7: 'Минимальная цена',
    8: 'Средневзвешенная цена',
    9: 'Максимальная цена',
    10: 'Рыночная цена',
    11: 'Лучшее предложение',
    12: 'Лучший спрос',
    13: 'Количество договоров, шт.'
}

excel_count_columns = 14


def read_table_pdf(file_name: str) -> Generator:
    with pdfplumber.open(file_name) as pdf_file:
        for index, page in enumerate(pdf_file.pages):
            yield index, page.extract_table()


def parse_pdf(table_pdf: Generator, file_date: datetime.date) -> list[dict]:
    result = []
    for index, table in table_pdf:
        if table is None:
            continue

        if index <= 2:
            table = table[2:]

        for row in table:
            if row[pdf_fields['count']] == '-':
                continue

            save_data = {
                'exchange_product_id': row[pdf_fields['exchange_product_id']],
                'exchange_product_name': row[pdf_fields['exchange_product_name']],
                'oil_id': row[pdf_fields['exchange_product_id']][:4],
                'delivery_basis_id': row[pdf_fields['exchange_product_id']][4:7],
                'delivery_basis_name': row[pdf_fields['exchange_product_id']][-1],
                'delivery_type_id': row[pdf_fields['exchange_product_id']][-1],
                'volume': row[pdf_fields['volume']],
                'total': row[pdf_fields['total']],
                'count': row[pdf_fields['count']],
                'date': file_date
            }
            result.append(save_data)

    return result


def get_table_xls(file_name: str) -> pd.DataFrame:
    df = pd.read_excel(file_name)

    rows, columns = df.shape

    cords = None
    for row in range(1, rows):
        for column in range(columns):
            if df.iloc[row, column] == 'Единица измерения: Метрическая тонна':
                cords = (row, column)
                break

    if cords is None:
        raise Exception('Таблица не найден')  # Изменить на кастомный класс

    df = df.iloc[cords[0] + 1:-2,1:]
    df.columns = [excel_fields[i] for i in range(excel_count_columns)]
    df = df.dropna(subset=[excel_fields[1]])
    df = df[2:]
    df.reset_index(drop=True, inplace=True)

    return df


def parse_xls(table: pd.DataFrame, file_date: datetime.date) -> list[dict]:
    df = table[pd.to_numeric(table[excel_fields[13]], errors='coerce') >= 1]

    result = []
    for index in range(len(df)):
        row = df.iloc[index]

        data = {
            'exchange_product_id': row[excel_fields[0]],
            'exchange_product_name': row[excel_fields[1]],
            'oil_id': row[excel_fields[0]][:4],
            'delivery_basis_id': row[excel_fields[0]][4:7],
            'delivery_basis_name': row[excel_fields[0]][-1],
            'delivery_type_id': row[excel_fields[0]][-1],
            'volume': row[excel_fields[3]],
            'total': row[excel_fields[4]],
            'count': row[excel_fields[13]],
            'date': file_date
        }
        result.append(data)

    return result

import pdfplumber

from datetime import datetime
from typing import Generator


fields = {
    'exchange_product_id': 0,
    'exchange_product_name': 1,
    'volume': 3,
    'total': 4,
    'count': -1
}


def read_table_pdf(file_name: str) -> Generator:
    with pdfplumber.open(file_name) as pdf_file:
        for index, page in enumerate(pdf_file.pages):
            yield index, page.extract_table()


def parse_pdf(table_pdf: Generator, file_date: datetime.date) -> list[dict]:
    result = []
    for index, table in table_pdf:

        if index == 0:
            table = table[2:]

        for row in table:
            if row[fields['count']] == '-':
                continue

            save_data = {
                'exchange_product_id': row[fields['exchange_product_id']],
                'exchange_product_name': row[fields['exchange_product_name']],
                'oil_id': row[fields['exchange_product_id']][:4],
                'delivery_basis_id': row[fields['exchange_product_id']][4:7],
                'delivery_basis_name': row[fields['exchange_product_id']][-1],
                'delivery_type_id': row[fields['exchange_product_id']][-1],
                'volume': row[fields['volume']],
                'total': row[fields['total']],
                'count': row[fields['count']],
                'date': file_date
            }
            result.append(save_data)

    return result

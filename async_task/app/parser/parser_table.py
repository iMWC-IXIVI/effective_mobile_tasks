import pandas as pd

from typing import Optional

from datetime import datetime

from model_validate import ValidateData
from core import settings


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

excel_fields = {
    0: 'Код инструмента',
    1: 'Наименование инструмента',
    2: 'Базис поставки',
    3: 'Объем договоров в единицах измерения',
    4: 'Объем договоров, руб.',
    5: 'Изменение цены к цене предыдущего дня (руб.)',
    6: 'Изменение цены к цене предыдущего дня (%)',
    7: 'Минимальная цена',
    8: 'Средневзвешенная цена',
    9: 'Максимальная цена',
    10: 'Рыночная цена',
    11: 'Цена заявки (Лучшее предложение)',
    12: 'Цена заявки (Лучший спрос)',
    13: 'Количество сделок шт.'
}


def read_table(file_name: str) -> Optional[pd.DataFrame]:
    """Формирование DataFrame таблицы"""

    df: pd.DataFrame = pd.read_excel(file_name)

    rows, columns = df.shape

    cords = None
    for row in range(rows):
        for column in range(1, columns):
            if df.iloc[row, column] == 'Единица измерения: Метрическая тонна':
                cords = (row, column)
                break
        if cords:
            break

    len_first_column = len(df.iloc[rows//2, 1])
    minus = 0
    while len(df.iloc[rows - 1, 1]) != len_first_column:
        minus += 1
        rows -= 1

    df = df.iloc[cords[0]:-minus, cords[1]:]
    df = df.dropna(axis=1, how='all')
    df.columns = [excel_fields[index] for index in range(14)]
    df = df[3:]
    df = df.dropna(subset=df.columns[1:], how='all')
    df.reset_index(drop=True, inplace=True)

    return df


def parse_data_frame(df: pd.DataFrame) -> list[ValidateData]:
    """Валидация данных из таблиц"""

    return [ValidateData(**row.to_dict()) for _, row in df.iterrows()]


def main():
    """Перенести в main.py TODO"""

    files_list = settings.DOWNLOAD_DIR.glob('*.xls')
    range_dates = [datetime(year=2019, month=1, day=1).date(), datetime(year=2026, month=1, day=1).date()]

    result_data = []
    for file_path in files_list:
        date_name = datetime.strptime(file_path.stem, '%d.%m.%Y')
        if range_dates[0] <= date_name.date() < range_dates[1]:
            df = read_table(file_path)
            result_data.extend(parse_data_frame(df))


if __name__ == '__main__':
    main()

import pandas as pd

from typing import Optional

from .model_validate import ValidateData


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

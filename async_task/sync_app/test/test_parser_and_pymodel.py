import pathlib
import pytest

from parser import read_table, parse_data_frame, ValidateData


@pytest.fixture()
def get_file():
    """Получение абсолютного пути до файла"""

    return pathlib.Path(__file__).resolve().parent/'fixtures'/'test_table.xls'


def test_get_dataframe(get_file: pathlib.Path) -> None:
    """Проверка получения dataframe"""

    shape = (499, 14)
    name_columns = [
        'Код инструмента',
        'Наименование инструмента',
        'Базис поставки',
        'Объем договоров в единицах измерения',
        'Объем договоров, руб.',
        'Изменение цены к цене предыдущего дня (руб.)',
        'Изменение цены к цене предыдущего дня (%)',
        'Минимальная цена',
        'Средневзвешенная цена',
        'Максимальная цена',
        'Рыночная цена',
        'Цена заявки (Лучшее предложение)',
        'Цена заявки (Лучший спрос)',
        'Количество сделок шт.'
    ]
    code_item = 'A001KRU060F'
    best_price = '91500'

    df = read_table(str(get_file))
    first_row = df.iloc[0]

    assert df.shape == shape
    assert df.columns.tolist() == name_columns
    assert first_row['Код инструмента'] == code_item
    assert first_row['Цена заявки (Лучшее предложение)'] == best_price


def test_parse_df_to_data_class(get_file: pathlib.Path) -> None:
    """Проверка Pydantic модели parse_data_frame"""

    data = {
        'Код инструмента': 'A001KRU060F',
        'Наименование инструмента': 'Бензин (АИ-100-К5), ст. Круглое Поле (ст. отправления)',
        'Базис поставки': 'ст. Круглое Поле',
        'Объем договоров в единицах измерения': '-',
        'Объем договоров, руб.': '-',
        'Изменение цены к цене предыдущего дня (руб.)': '-',
        'Изменение цены к цене предыдущего дня (%)': '-',
        'Минимальная цена': '-',
        'Средневзвешенная цена': '-',
        'Максимальная цена': '-',
        'Рыночная цена': '-',
        'Цена заявки (Лучшее предложение)': '91500',
        'Цена заявки (Лучший спрос)': '-',
        'Количество сделок шт.': '-'
    }
    valid_data = ValidateData(**data)
    len_valid_data = 499

    df = read_table(str(get_file))
    df_valid_data = parse_data_frame(df)

    first_item = df_valid_data[0]

    assert first_item == valid_data
    assert len(df_valid_data) == len_valid_data

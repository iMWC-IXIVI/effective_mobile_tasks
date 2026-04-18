import logging
import time
import random

from datetime import datetime

from typing import Generator

from core import settings, setup_logger
from downloader import get_page, get_urls_and_names_files, download_file, get_url_next_page
from parser import read_table, parse_data_frame, ValidateData
from database import save_data
from utils.decorators import timer


setup_logger()


@timer
def crawl_and_download(url: str) -> None:
    """Обход всех страниц и скачивание файлов синхронно"""

    while url:
        try:
            logging.info(f'url, откуда скачиваются все файлы - {url}')

            response = get_page(url)

            datas = get_urls_and_names_files(response)

            for link, file_name in datas:
                download_file(link, file_name)
                time.sleep(random.uniform(0, 1))

            time.sleep(random.uniform(2, 4))

            url = get_url_next_page(response)
        except Exception as e:
            logging.error(f'Произошла ошибка по {url} - {e}')
            logging.info(f'Перезапуск функции через 10 секунд')
            time.sleep(10)


def read_and_parse() -> Generator[list[ValidateData], None, None]:
    """Чтение файлов и создание дата классов для будущего сохранения"""

    files_list = settings.DOWNLOAD_DIR.glob('*.xls')
    range_dates = [datetime(year=2019, month=1, day=1).date(), datetime(year=2026, month=1, day=1).date()]

    for file_path in files_list:
        date_file = datetime.strptime(file_path.stem, '%d.%m.%Y').date()

        if range_dates[0] <= date_file < range_dates[1]:
            try:
                df = read_table(file_path)
                yield parse_data_frame(df)
            except Exception as e:
                logging.error(f'Ошибка в прочтении или создании дата класса - {e}')


@timer
def save_from_data_class() -> None:
    """Сохранение данных в БД"""

    for data in read_and_parse():
        try:
            save_data(data)
        except Exception as e:
            logging.error(f'Во время сохранения данных произошла ошибка - {e}')

        logging.info(f'Данные успешно сохранены')


@timer
def main():
    crawl_and_download(settings.SPIMEX_LIST)
    save_from_data_class()


if __name__ == '__main__':
    main()

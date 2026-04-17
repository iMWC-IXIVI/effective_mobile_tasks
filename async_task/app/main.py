import logging
import asyncio
import random
import aiohttp

from datetime import datetime

from typing import AsyncGenerator

from core import settings
from downloader import get_page, get_urls_and_names_files, download_file, get_url_next_page
from parser import read_table, parse_data_frame, ValidateData
from database import save_data


async def crawl_and_download(url: str) -> None:
    """Обход всех страниц и скачивание файлов асинхронно"""

    async with aiohttp.ClientSession(headers=settings.HEADERS) as session:
        while url:
            try:
                response = await get_page(session, url)

                datas = get_urls_and_names_files(response)

                tasks = [download_file(link, file_name, session) for link, file_name in datas]

                await asyncio.gather(*tasks)
                await asyncio.sleep(random.uniform(2, 4))

                url = get_url_next_page(response)
            except Exception as e:
                logging.error(f'Произошла ошибка по {url} - {e}')
                logging.info(f'Перезапуск функции через 10 секунд')
                await asyncio.sleep(10)


async def read_and_parse() -> AsyncGenerator[list[ValidateData], None]:
    """Чтение файлов и создание дата классов для будущего сохранения"""

    loop = asyncio.get_running_loop()
    files_list = settings.DOWNLOAD_DIR.glob('*.xls')
    range_dates = [datetime(year=2019, month=1, day=1).date(), datetime(year=2026, month=1, day=1).date()]

    for file_path in files_list:
        date_file = datetime.strptime(file_path.stem, '%d.%m.%Y').date()

        if range_dates[0] <= date_file < range_dates[1]:
            try:
                df = await loop.run_in_executor(None, read_table, file_path)
                yield parse_data_frame(df)
            except Exception as e:
                logging.error(f'Ошибка в прочтении или создании дата класса - {e}')


async def save_from_data_class() -> None:
    """Сохранение данных в БД"""

    async def save_one(data):
        """Применение семафора к задачам"""
        try:
            async with settings.DATABASE_SEMAPHORE:
                await save_data(data)
        except Exception as e:
            logging.error(f'Во время формирования задачи произошла ошибка - {e}')

    tasks = [save_one(data) async for data in read_and_parse()]

    await asyncio.gather(*tasks)


async def main():
    await crawl_and_download(settings.SPIMEX_LIST)
    await save_from_data_class()


if __name__ == '__main__':
    asyncio.run(main())

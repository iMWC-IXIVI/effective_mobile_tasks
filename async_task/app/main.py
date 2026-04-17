import logging
import asyncio
import random
import aiohttp

from core import settings
from downloader import get_page, get_urls_and_names_files, download_file, get_url_next_page


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


async def main():
    await crawl_and_download(settings.SPIMEX_LIST)


if __name__ == '__main__':
    asyncio.run(main())

import random
import asyncio
import aiohttp

from typing import Iterator, Optional

from bs4 import BeautifulSoup

from core import settings

from download_files import download_file


async def get_page(session: aiohttp.ClientSession, url: str) -> str:
    """Получение страницы сайта"""

    async with session.get(url) as response:
        response.raise_for_status()
        return await response.text()


def get_urls_and_names_files(response: str) -> Iterator[tuple[str, str]]:
    """Получение названий url-ов для скачивания + названия для файлов"""

    parser_page = BeautifulSoup(response, 'html.parser')
    div_page_content = parser_page.find('div', class_='page-content__tabs__block', attrs={'data-tabcontent': '1'})
    div_accordeon_inner = div_page_content.find('div', class_='accordeon-inner')
    a_files = div_accordeon_inner.find_all('a', class_='accordeon-inner__item-title link xls')

    if not a_files:
        return iter([])

    p_dates = div_accordeon_inner.find_all('p')

    if len(a_files) != len(p_dates):
        p_dates = p_dates[len(p_dates) - len(a_files):]

    hrefs = (settings.SPIMEX_BASE_URL + a.get('href') for a in a_files)
    dates = (p.find('span').text + settings.PREFIX_FILE for p in p_dates)

    return zip(hrefs, dates, strict=True)


def get_url_next_page(response: str) -> Optional[str]:
    """Возвращение url следующей страницы"""

    parser_page = BeautifulSoup(response, 'html.parser')
    next_page = parser_page.find('li', class_='bx-pag-next')

    href = next_page.find('a')

    if href is None:
        return None

    return settings.SPIMEX_BASE_URL + href.get('href')


async def main(url: str) -> None:
    async with aiohttp.ClientSession(headers=settings.HEADERS) as session:
        while url:
            response = await get_page(session, url)

            data = get_urls_and_names_files(response)

            tasks = [download_file(link, file_name, session) for link, file_name in data]

            await asyncio.gather(*tasks)
            await asyncio.sleep(random.uniform(2, 4))

            url = get_url_next_page(response)


if __name__ == '__main__':
    asyncio.run(main(settings.SPIMEX_LIST))

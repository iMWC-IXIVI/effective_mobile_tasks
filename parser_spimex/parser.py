import bs4 as bs

from datetime import datetime
from urllib import request

from core import SRC_PATH


BASE_URL = 'https://spimex.com/'
URL = 'https://spimex.com/markets/oil_products/trades/results/'
BASE_DATE = datetime.strptime('01.01.2023', '%d.%m.%Y').date()


def get_html(url: str) -> bs.BeautifulSoup:
    """Получение HTML страницы"""
    response = request.urlopen(url=url)
    parse = bs.BeautifulSoup(response.read(), 'html.parser')
    response.close()

    return parse


def parse_html(parse: bs.BeautifulSoup) -> list[tuple[str, str]] | tuple[list[tuple[str, str]], str]:
    """Получение ссылки для скачивания + имя файла"""
    div_inner_item_lst = None
    result = []

    main_div = parse.find_all('div', class_='page-content__tabs__block')
    for div in main_div:
        if div.get('data-tabcontent') == '1':
            div_inner_item_lst = div.find_all('div', class_='accordeon-inner__wrap-item')

    if div_inner_item_lst is None:
        return result

    for div_inner_item in div_inner_item_lst:
        a_link = div_inner_item.find('a', class_='accordeon-inner__item-title link pdf')

        if a_link is None:
            a_link = div_inner_item.find('a', class_='accordeon-inner__item-title link xls')
            prefix = '.xls'
        else:
            prefix = '.pdf'

        p_date = div_inner_item.find('p')
        file_date = p_date.find('span').text

        file_dt = datetime.strptime(file_date, '%d.%m.%Y').date()
        if file_dt <= BASE_DATE:
            return result

        file_name = file_date + prefix
        download_url = BASE_URL + a_link.get('href')

        result.append((download_url, file_name))

    li_next_page_link = parse.find('li', class_='bx-pag-next')
    a_li_next_page_link = li_next_page_link.find('a')
    next_page = a_li_next_page_link.get('href')

    return result, BASE_URL + next_page


def download_file(lst_urls: list[tuple[str, str]]) -> None:
    """Загрузка файла"""
    for url, file_path in lst_urls:
        request.urlretrieve(url, SRC_PATH/file_path)


def main(url: str):
    parse = get_html(url)
    urls = parse_html(parse)

    if isinstance(urls, tuple):
        download_file(urls[0])
        main(urls[1])
    elif isinstance(urls, list):
        download_file(urls)

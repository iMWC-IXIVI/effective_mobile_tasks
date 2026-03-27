import bs4 as bs

from urllib import request

from core import SRC_PATH


BASE_URL = 'https://spimex.com/'
URL = 'https://spimex.com/markets/oil_products/trades/results/'


def get_html() -> bs.BeautifulSoup:
    """Получение HTML страницы"""
    response = request.urlopen(url=URL)
    parse = bs.BeautifulSoup(response.read(), 'html.parser')
    response.close()

    return parse


def parse_html(parse: bs.BeautifulSoup) -> tuple[str, str]:
    """Получение ссылки для скачивания + имя файла"""
    div_inner_item = parse.find('div', class_='accordeon-inner__item')

    a_link = div_inner_item.find('a', class_='accordeon-inner__item-title link pdf')
    p_date = div_inner_item.find('p')

    file_name = p_date.find('span').text + '.pdf'
    download_url = BASE_URL + a_link.get('href')

    return download_url, file_name


def download_file(url: str, file_path: str) -> None:
    """Загрузка файла"""
    request.urlretrieve(url, SRC_PATH/file_path)

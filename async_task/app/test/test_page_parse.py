import pytest
import pathlib

from downloader import get_urls_and_names_files, get_url_next_page


@pytest.fixture()
def get_html():
    """Загрузка html страницы"""
    filepath = pathlib.Path(__file__).parent/'fixtures'/'spimex_test.html'

    with open(filepath, 'r', encoding='utf-8') as html_file:
        html = html_file.read()

    return html


def test_parse_page(get_html) -> None:
    """Проверка get_urls_and_names_files"""

    data = list(get_urls_and_names_files(get_html))

    len_data = len(data)
    filenames = [
        '04.09.2025.xls',
        '03.09.2025.xls',
        '02.09.2025.xls',
        '01.09.2025.xls',
        '29.08.2025.xls',
        '28.08.2025.xls',
        '27.08.2025.xls',
        '26.08.2025.xls',
        '25.08.2025.xls',
        '22.08.2025.xls'
    ]

    assert len_data == 10

    for href, filename in data:
        assert href.startswith('https://spimex.com/files/trades/result/oil_xls/')
        assert filename in filenames


def test_get_next_page(get_html) -> None:
    """Проверка get_url_next_page"""

    href_fixture = 'https://spimex.com/markets/oil_products/trades/results/?page=page-17'

    href = get_url_next_page(get_html)

    assert href == href_fixture

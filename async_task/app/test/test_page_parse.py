import pytest

from downloader import get_urls_and_names_files, get_url_next_page


@pytest.fixture()
def get_html():
    """Загрузка html страницы"""
    with open('fixtures/spimex_test.html', 'r', encoding='utf-8') as html_file:
        html = html_file.read()

    return html


def test_parse_page(get_html) -> None:
    """Проверка get_urls_and_names_files"""

    data = list(get_urls_and_names_files(get_html))

    len_data = len(data)
    filenames = [
        '05.09.2025.xls',
        '08.09.2025.xls',
        '09.09.2025.xls',
        '10.09.2025.xls',
        '11.09.2025.xls',
        '12.09.2025.xls',
        '15.09.2025.xls',
        '16.09.2025.xls',
        '17.09.2025.xls',
        '18.09.2025.xls'
    ]

    assert len_data == 10

    for href, filename in data:
        assert href.startswith('https://spimex.comhttps://spimex.com/files/trades/result/oil_xls/') is True
        assert filename in filenames


def test_get_next_page(get_html) -> None:
    """Проверка get_url_next_page"""

    href_fixture = 'https://spimex.comhttps://spimex.com/markets/oil_products/trades/results/?page=page-16'

    href = get_url_next_page(get_html)

    assert href == href_fixture

import datetime
from datetime import date

from bs4 import BeautifulSoup


def parse_page_links(html: str, start_date: date, end_date: date, url: str | None = None):
    """
    Парсит страницы на бюллетени для извлечения даты в диапазоне дат

    :param html: str (страница)
    :param start_date: date (старт диапазона в формате date)
    :param end_date: date (конце диапазона в формате date)
    :param url: str | None = None (ссылка для формирования результата)
    """
    results = []
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a", class_="accordeon-inner__item-title link xls")
    base_url = url if url is not None else "https://spimex.com"
    base_href_url = "/upload/reports/oil_xls/oil_xls_"

    for link in links:
        link_href = link.get("href")
        if not link_href:
            continue

        href = link_href.split("?")[0]
        if base_href_url not in href or not href.endswith(".xls"):
            continue

        try:
            date_href = href.split("oil_xls_")[1][:8]  # TODO Добавил бы регулярное выражения для извлечение даты
            date_file = datetime.datetime.strptime(date_href, "%Y%m%d").date()
            if start_date <= date_file <= end_date:
                result_link = href if href.startswith("http") else f"{base_url}{href}"
                results.append((result_link, date_file))
            else:
                print(f"Ссылка {href} вне диапазона дат")
        except Exception as e:
            print(f"Не удалось извлечь дату из ссылки {href}: {e}")

    return results

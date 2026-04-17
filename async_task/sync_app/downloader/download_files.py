import requests

from core import settings


def download_file(link: str, file_name: str) -> None:
    """Загрузка файла из сайта"""

    with requests.get(link, headers=settings.HEADERS) as response:
        response.raise_for_status()
        with open(settings.DOWNLOAD_DIR/file_name, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

import sys
import logging
import datetime

from logging.handlers import RotatingFileHandler
from pathlib import Path

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DOWNLOAD_DIR: Path = BASE_DIR/'src'
    LOGS_DIR: Path = BASE_DIR/'logs'

    SPIMEX_BASE_URL: str = 'https://spimex.com'
    SPIMEX_LIST: str = SPIMEX_BASE_URL + '/markets/oil_products/trades/results/'

    PREFIX_FILE: str = '.xls'

    MAXIMUM_RETRIES: int = 10

    HEADERS: dict = {
        'sec-ch-ua': '"Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Mobile Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://spimex.com/markets/oil_products/trades/results/',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
    }

    SYNC_DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent/'.env',
        extra='ignore'
    )

    @model_validator(mode='after')
    def _check_or_create_src(self) -> 'Settings':
        """Проверка и создание папки src в базовой директории проекта"""

        if not self.DOWNLOAD_DIR.exists():
            self.DOWNLOAD_DIR.mkdir()
        return self

    @model_validator(mode='after')
    def _check_or_create_logs(self) -> 'Settings':
        """Проверка и создание папки logs в базовой директории проекта"""
        if not self.LOGS_DIR.exists():
            self.LOGS_DIR.mkdir()
        return self


def setup_logger() -> None:
    """Настройка логирования"""

    filename = datetime.datetime.now().strftime('%d-%m-%Y') + '.log'
    filepath = settings.LOGS_DIR/filename

    console_formatter = logging.Formatter(
        fmt='%(asctime)s | %(name)s (%(levelname)s) - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_formatter = logging.Formatter(
        fmt='%(asctime)s | %(pathname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.INFO)

    file_handler = RotatingFileHandler(filename=filepath, mode='a', encoding='utf-8', maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.ERROR)

    logger = logging.getLogger()

    logger.setLevel(logging.INFO)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)


settings = Settings()

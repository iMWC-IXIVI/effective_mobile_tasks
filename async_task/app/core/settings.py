from pathlib import Path

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DOWNLOAD_DIR: Path = BASE_DIR/'src'

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent/'.env',
        extra='ignore'
    )

    @model_validator(mode='after')
    def _check_or_create(self) -> 'Settings':
        """Проверка и создание папки src в базовой дирректории проекта"""

        if not self.DOWNLOAD_DIR.exists():
            self.DOWNLOAD_DIR.mkdir()
        return self


settings = Settings()

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки проекта"""

    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR.parent/'.env',
        extra='ignore'
    )


settings = Settings()

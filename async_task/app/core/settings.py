from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DOWNLOAD_DIR: Path = BASE_DIR/'src'

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent/'.env',
        extra='ignore'
    )


settings = Settings()

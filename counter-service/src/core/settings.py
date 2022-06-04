from pathlib import Path

from pydantic import BaseSettings

ROOT_DIR = Path(__file__).parent


class Settings(BaseSettings):
    database_url: str = "sqlite:///./app.db"

    debug: bool = False


settings = Settings()

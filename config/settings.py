from pydantic import BaseSettings
from enum import Enum

__all__ = ['settings']


class _Settings(BaseSettings):
    # Application Settings
    hash_algorithm: str = "SHA-512"
    pass_salt: str = "nosalt"
    database_url: str = "sqlite:///./app.db"
    admin_login: str = "admin"
    auth_secret_token: str = None
    access_token_expire_minutes: int = 60

    class EnvMode(str, Enum):
        prod = "PROD"
        dev = "DEV"

    ENV: EnvMode = EnvMode.prod

    @property
    def is_production(self):
        return self.ENV == self.EnvMode.prod

    # Logging Settings
    @property
    def logging_level(self):
        return 'INFO' if self.is_production else 'DEBUG'


settings = _Settings()

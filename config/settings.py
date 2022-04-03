from typing import List
from pydantic import BaseSettings, BaseModel
from enum import Enum

__all__ = ('settings',)


class DbConnection(BaseModel):
    host: str
    port: int


class _Settings(BaseSettings):
    # Application Settings
    hash_algorithm: str = "SHA-512"
    pass_salt: str = "nosalt"
    access_token_expire_minutes: int = 60
    db_host: str = 'localhost'
    db_port: int = 3306
    db_name: str = 'social_network'
    db_user: str = 'social_network'
    db_password: str = ''
    db_replicas: List[DbConnection] = []

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

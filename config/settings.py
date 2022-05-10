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
    redis_host: str = 'localhost'
    redis_port: int = 6379
    amqp_url: str = 'amqp://guest:guest@localhost/'


settings = _Settings()

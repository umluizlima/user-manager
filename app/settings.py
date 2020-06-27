from enum import Enum
from functools import lru_cache
from typing import Optional

from pydantic import BaseSettings, EmailStr


class Environment(str, Enum):
    DEVELOPMENT = "dev"
    PRODUCTION = "prod"


class Settings(BaseSettings):
    ENV: Environment = Environment.DEVELOPMENT
    SENTRY_DSN: str = None
    API_KEY: str = "you-will-want-something-safe-here"
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost/user-manager"
    BROKER_URL: str = "amqp://rabbitmq:rabbitmq@localhost"
    JWT_ALGORITHM: str = "RS256"
    JWT_PUBLIC_KEY: bytes
    JWT_PRIVATE_KEY: bytes

    class Config:
        env_file = ".env"
        case_sensitive = True
        fields = {"BROKER_URL": {"env": ["BROKER_URL", "CLOUDAMQP_URL"]}}


@lru_cache
def get_settings():
    return Settings()

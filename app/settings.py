from enum import Enum
from functools import lru_cache

from pydantic import BaseSettings


class Environment(str, Enum):
    DEVELOPMENT = "dev"
    PRODUCTION = "prod"


class Settings(BaseSettings):
    ENV: Environment = Environment.DEVELOPMENT
    SENTRY_DSN: str = None
    API_KEY: str = "you-will-want-something-safe-here"
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost/user-manager"
    CACHE_URL: str = "redis://:@localhost:6379/0"
    BROKER_URL: str = "amqp://rabbitmq:rabbitmq@localhost"
    JWT_ALGORITHM: str = "RS256"
    JWT_PUBLIC_KEY: bytes
    JWT_PRIVATE_KEY: bytes
    ACCESS_TOKEN_EXPIRATION_SECONDS: int = 1800
    SESSION_EXPIRATION_SECONDS: int = 604_800
    ACCESS_CODE_LENGTH: int = 6
    ACCESS_CODE_EXPIRATION_SECONDS: int = 300

    class Config:
        env_file = ".env"
        case_sensitive = True
        fields = {"BROKER_URL": {"env": ["BROKER_URL", "CLOUDAMQP_URL"]}}


@lru_cache
def get_settings():
    return Settings()

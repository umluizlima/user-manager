from enum import Enum
from typing import Optional

from pydantic import BaseSettings, EmailStr


class Environment(str, Enum):
    DEVELOPMENT = "dev"
    PRODUCTION = "prod"


class Settings(BaseSettings):
    ENV: Environment = Environment.DEVELOPMENT
    SENTRY_DSN: str = None
    API_KEY: str = "you-will-want-something-safe-here"
    BROKER_URL: str = "amqp://rabbitmq:rabbitmq@localhost"

    class Config:
        env_file = ".env"
        case_sensitive = True
        fields = {"BROKER_URL": {"env": ["BROKER_URL", "CLOUDAMQP_URL"]}}


settings = Settings()

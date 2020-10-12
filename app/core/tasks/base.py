from enum import Enum

from celery import Celery

from app.settings import Settings


class Task(str, Enum):
    SEND_TRANSACTIONAL = "SEND_TRANSACTIONAL"


def get_celery_app(name: str, broker_url: str, **kwargs):
    return Celery(name, broker=broker_url, **kwargs)

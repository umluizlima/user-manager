from functools import lru_cache

from app.settings import Settings

from .base import get_celery_app


@lru_cache
def get_tasks_producer(broker_url: str, **kwargs):
    return get_celery_app("producer", broker_url, **kwargs)


class TasksProducer:
    def __init__(self, settings: Settings):
        self._settings = settings
        self._producer = get_tasks_producer(self._settings.BROKER_URL)

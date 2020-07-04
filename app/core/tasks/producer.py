from functools import lru_cache

from app.settings import Settings

from .base import get_celery_app


@lru_cache
def get_tasks_producer(settings: Settings):
    return get_celery_app("producer", settings)


class TasksProducer:
    def __init__(self, settings: Settings):
        self._settings = settings
        self._producer = get_tasks_producer(self._settings)

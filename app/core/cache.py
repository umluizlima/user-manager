from functools import lru_cache

from redis import Redis

from ..settings import Settings


@lru_cache
def get_redis_client(cache_url: str) -> Redis:
    return Redis.from_url(cache_url)


class Cache:
    def __init__(self, settings: Settings):
        self._client = get_redis_client(settings.CACHE_URL)

    def get_client(self):
        return self._client

from functools import lru_cache

from redis import Redis


@lru_cache
def get_cache_client(cache_url: str) -> Redis:
    return Redis.from_url(cache_url)

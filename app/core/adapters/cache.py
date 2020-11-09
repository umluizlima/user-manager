from sys import maxsize
from typing import Optional

from redis import Redis


class CacheAdapter:
    def __init__(self, cache_client: Redis):
        self._client = cache_client

    def set_with_expiration(self, key: str, seconds: int, value: str):
        self._client.setex(key, seconds, value)

    def get(self, key: str) -> Optional[str]:
        value = self._client.get(key)
        return value.decode("utf-8") if value else None

    def delete(self, key: str):
        self._client.delete(key)

    def add_to_set(self, key: str, value: str):
        self._client.sadd(key, value)

    def is_in_set(self, key: str, value: str) -> bool:
        return bool(self._client.sismember(key, value))

    def remove_from_set(self, key: str, value: str):
        self._client.srem(key, value)

    def empty_set(self, key: str):
        self._client.spop(key, maxsize)

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

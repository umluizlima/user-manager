from random import randrange

from app.core.adapters import CacheAdapter
from app.settings import Settings


class CodeService:
    def __init__(self, settings: Settings, cache_adapter: CacheAdapter):
        self._settings = settings
        self._cache_adapter = cache_adapter

    def generate_code(self, key: str) -> str:
        access_code = self._generate_random_code()
        self._cache_adapter.set_with_expiration(
            key, self._settings.ACCESS_CODE_EXPIRATION_SECONDS, access_code
        )
        return access_code

    def verify_code(self, key: str, code: str) -> bool:
        cached_code = self._cache_adapter.get(key)
        if code != cached_code:
            return False
        self._cache_adapter.delete(key)
        return True

    def _generate_random_code(self) -> str:
        code = randrange(1, 10 ** self._settings.ACCESS_CODE_LENGTH)
        formatted_code = f"{code}".zfill(self._settings.ACCESS_CODE_LENGTH)
        return formatted_code

from random import randrange

from app.core.adapters import CacheAdapter
from app.settings import Settings


class AccessCodeService:
    def __init__(self, settings: Settings, cache_adapter: CacheAdapter):
        self._settings = settings
        self._cache_adapter = cache_adapter

    def generate_code(self, user_id: int) -> str:
        access_code = self._generate_random_code(self._settings.ACCESS_CODE_LENGTH)
        self._cache_adapter.set_with_expiration(
            self._get_access_code_key(user_id),
            self._settings.ACCESS_CODE_EXPIRATION_SECONDS,
            access_code,
        )
        return access_code

    def verify_code(self, user_id: int, code: str) -> bool:
        key = self._get_access_code_key(user_id)
        cached_code = self._cache_adapter.get(key)
        if code != cached_code:
            return False
        self._cache_adapter.delete(key)
        return True

    @staticmethod
    def _generate_random_code(length: int) -> str:
        code = randrange(1, 10 ** length)
        formatted_code = f"{code}".zfill(length)
        return formatted_code

    @staticmethod
    def _get_access_code_key(user_id: int) -> str:
        return f"user:{user_id}:access_code"

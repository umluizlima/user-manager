from random import randrange

from app.settings import Settings

from ..cache import Cache


class CodeService:
    def __init__(self, settings: Settings, cache_client: Cache):
        self._settings = settings
        self._cache = cache_client

    def generate_code(self, key: str) -> str:
        code = self._get_random_code()
        self._cache.setex(key, self._settings.ACCESS_CODE_EXPIRATION_SECONDS, code)
        return code

    def verify_code(self, key: str, code: str) -> bool:
        cached_code = self._cache.get(key)
        if not cached_code:
            return False
        return code == cached_code.decode("utf-8")

    def _get_random_code(self) -> str:
        code = randrange(1, 10 ** self._settings.ACCESS_CODE_LENGTH)
        formatted_code = f"{code}".zfill(self._settings.ACCESS_CODE_LENGTH)
        return formatted_code

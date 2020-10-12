from fastapi import Depends

from app.core.adapters import CacheAdapter
from app.core.cache import get_cache_client
from app.core.services import CodeService
from app.settings import get_settings, Settings


def cache_client(settings: Settings = Depends(get_settings)):
    return get_cache_client(settings.CACHE_URL)


def cache_adapter(cache_client=Depends(cache_client)):
    return CacheAdapter(cache_client)


def code_service(
    settings: Settings = Depends(get_settings),
    cache_adapter: CacheAdapter = Depends(cache_adapter),
):
    return CodeService(settings, cache_adapter)

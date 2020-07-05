from fastapi import Depends

from app.core.cache import Cache
from app.core.services import CodeService
from app.settings import get_settings, Settings


def cache_client(settings: Settings = Depends(get_settings)):
    return Cache(settings).get_client()


def code_service(
    settings: Settings = Depends(get_settings),
    cache_client: Cache = Depends(cache_client),
):
    return CodeService(settings, cache_client)

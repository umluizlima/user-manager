from time import sleep

from pytest import fixture

from app.core.adapters import CacheAdapter
from app.core.services import CodeService


@fixture
def cache_adapter(cache_client):
    return CacheAdapter(cache_client)


@fixture
def code_service(settings, cache_adapter):
    return CodeService(settings, cache_adapter)


def test_code_service_stores_code_in_cache(code_service):
    code = code_service.generate_code("key")
    assert code_service._cache_adapter.get("key") == code


def test_code_service_verifies_valid_code(code_service):
    code = code_service.generate_code("key")
    assert code_service.verify_code("key", code)


def test_code_service_deletes_verified_code(code_service):
    code = code_service.generate_code("key")
    code_service.verify_code("key", code)
    assert not code_service._cache_adapter.get("key")


def test_code_service_does_not_verify_expired_code(cache_adapter, settings):
    settings.ACCESS_CODE_EXPIRATION_SECONDS = 1
    code_service = CodeService(settings, cache_adapter)
    code = code_service.generate_code("key")
    sleep(1.001)
    assert not code_service.verify_code("key", code)

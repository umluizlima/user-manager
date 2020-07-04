from time import sleep

from pytest import fixture

from app.core.services import CodeService


@fixture
def code_service(cache_client, settings):
    return CodeService(settings, cache_client)


def test_code_service_verifies_valid_code(code_service):
    code = code_service.generate_code("key")
    assert code_service.verify_code("key", code)


def test_code_service_does_not_verify_expired_code(cache_client, settings):
    settings.ACCESS_CODE_EXPIRATION_SECONDS = 1
    code_service = CodeService(settings, cache_client)
    code = code_service.generate_code("key")
    sleep(1.001)
    assert not code_service.verify_code("key", code)

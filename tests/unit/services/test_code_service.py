from unittest.mock import MagicMock

from pytest import fixture

from app.core.services import CodeService

cache_client = MagicMock()
key = "abc"


@fixture
def code_service(settings):
    cache_client.reset_mock()
    return CodeService(settings, cache_client)


def test_code_service_generates_code_with_length(code_service, settings):
    code = code_service.generate_code(key)
    assert len(code) == settings.ACCESS_CODE_LENGTH


def test_code_service_generates_code_with_expiration(code_service, settings):
    code = code_service.generate_code(key)
    cache_client.set_with_expiration.assert_called_once_with(
        key, settings.ACCESS_CODE_EXPIRATION_SECONDS, code
    )


def test_code_service_verify_code_returns_false_if_not_exist(code_service):
    code = code_service.generate_code(key)
    cache_client.get.return_value = None
    assert not code_service.verify_code(key, code)


def test_code_service_verify_code_returns_false_if_not_match(code_service):
    code = code_service.generate_code(key)
    cache_client.get.return_value = f"{code}0".encode()
    assert not code_service.verify_code(key, code)


def test_code_service_verify_code_returns_true_if_match(code_service):
    code = code_service.generate_code(key)
    cache_client.get.return_value = code
    assert code_service.verify_code(key, code)


def test_code_service_verify_code_deletes_code_if_match(code_service):
    code = code_service.generate_code(key)
    cache_client.get.return_value = code
    code_service.verify_code(key, code)
    cache_client.delete.assert_called_once_with(key)

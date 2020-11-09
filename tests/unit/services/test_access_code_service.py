from unittest.mock import MagicMock

from pytest import fixture

from app.core.services import AccessCodeService

cache_adapter = MagicMock()
user_id = 123


@fixture
def access_code_service(settings):
    cache_adapter.reset_mock()
    return AccessCodeService(settings, cache_adapter)


def test_access_code_service_generates_code_with_length(access_code_service, settings):
    code = access_code_service.generate_code(user_id)
    assert len(code) == settings.ACCESS_CODE_LENGTH


def test_access_code_service_generates_code_with_expiration(
    access_code_service, settings
):
    code = access_code_service.generate_code(user_id)
    cache_adapter.set_with_expiration.assert_called_once_with(
        access_code_service._get_access_code_key(user_id),
        settings.ACCESS_CODE_EXPIRATION_SECONDS,
        code,
    )


def test_access_code_service_verify_code_returns_false_if_not_exist(
    access_code_service,
):
    code = access_code_service.generate_code(user_id)
    cache_adapter.get.return_value = None
    assert not access_code_service.verify_code(user_id, code)


def test_access_code_service_verify_code_returns_false_if_not_match(
    access_code_service,
):
    code = access_code_service.generate_code(user_id)
    cache_adapter.get.return_value = f"{code}0".encode()
    assert not access_code_service.verify_code(user_id, code)


def test_access_code_service_verify_code_returns_true_if_match(access_code_service):
    code = access_code_service.generate_code(user_id)
    cache_adapter.get.return_value = code
    assert access_code_service.verify_code(user_id, code)


def test_access_code_service_verify_code_deletes_code_if_match(access_code_service):
    code = access_code_service.generate_code(user_id)
    cache_adapter.get.return_value = code
    access_code_service.verify_code(user_id, code)
    cache_adapter.delete.assert_called_once_with(
        access_code_service._get_access_code_key(user_id)
    )

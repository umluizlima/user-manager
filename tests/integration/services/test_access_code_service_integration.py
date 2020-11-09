from time import sleep

from pytest import fixture

from app.core.services import AccessCodeService

user_id = 123


@fixture
def access_code_service(settings, cache_adapter):
    return AccessCodeService(settings, cache_adapter)


def test_access_code_service_stores_code_in_cache(access_code_service):
    code = access_code_service.generate_code(user_id)
    stored_code = access_code_service._cache_adapter.get(
        access_code_service._get_access_code_key(user_id)
    )
    assert stored_code == code


def test_access_code_service_verifies_valid_code(access_code_service):
    code = access_code_service.generate_code(user_id)
    assert access_code_service.verify_code(user_id, code)


def test_access_code_service_deletes_verified_code(access_code_service):
    code = access_code_service.generate_code(user_id)
    access_code_service.verify_code(user_id, code)
    assert not access_code_service._cache_adapter.get(user_id)


def test_access_code_service_does_not_verify_expired_code(cache_adapter, settings):
    settings.ACCESS_CODE_EXPIRATION_SECONDS = 1
    access_code_service = AccessCodeService(settings, cache_adapter)
    code = access_code_service.generate_code(user_id)
    sleep(1.001)
    assert not access_code_service.verify_code(user_id, code)

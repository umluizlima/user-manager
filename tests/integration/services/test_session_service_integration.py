from time import sleep

from pytest import fixture

from app.core.services import SessionService

user_id = 123


@fixture
def session_service(settings, cache_adapter):
    return SessionService(settings, cache_adapter)


def test_session_service_should_store_user_sessions_in_cache(session_service):
    session = session_service.generate_session(user_id)
    assert session_service._cache_adapter.is_in_set(
        session_service._get_sessions_key(user_id), session,
    )


def test_session_service_should_store_session_in_cache(session_service):
    session = session_service.generate_session(user_id)
    assert bool(
        session_service._cache_adapter.get(session_service._get_session_key(session))
    )


def test_session_service_should_verify_valid_session(session_service):
    session = session_service.generate_session(user_id)
    assert session_service.verify_session(user_id, session)


def test_session_service_should_not_verify_invalid_session(session_service):
    assert not session_service.verify_session(user_id, "abcdef")


def test_session_service_should_not_verify_expired_session(cache_adapter, settings):
    settings.SESSION_EXPIRATION_SECONDS = 1
    session_service = SessionService(settings, cache_adapter)
    session = session_service.generate_session(user_id)
    sleep(1.001)
    assert not session_service.verify_session(user_id, session)


def test_session_service_should_revoke_single_session(cache_adapter, session_service):
    session = session_service.generate_session(user_id)
    session_service.revoke_session(user_id, session)
    assert not cache_adapter.is_in_set(
        session_service._get_sessions_key(user_id), session,
    )


def test_session_service_should_revoke_all_sessions(cache_adapter, session_service):
    sessions = [
        session_service.generate_session(user_id),
        session_service.generate_session(user_id),
    ]
    session_service.revoke_all_sessions(user_id)
    for session in sessions:
        assert not cache_adapter.is_in_set(
            session_service._get_sessions_key(user_id), session,
        )

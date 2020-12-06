from unittest.mock import MagicMock

from pytest import fixture
from starlette.testclient import TestClient

from app.api import create_api
from app.api.dependencies import send_code_producer
from app.core.services import JWTService, SessionService
from app.settings import get_settings

mock = MagicMock()


@fixture
def send_code_producer_mock():
    return mock


@fixture
def jwt_service(settings_with_rsa):
    return JWTService(settings_with_rsa)


@fixture
def session_service(cache_adapter, settings_with_rsa):
    return SessionService(settings_with_rsa, cache_adapter)


@fixture
def client(settings_with_rsa):
    api = create_api(settings_with_rsa)
    api.dependency_overrides[get_settings] = lambda: settings_with_rsa
    api.dependency_overrides[send_code_producer] = lambda: mock
    client = TestClient(api)
    return client

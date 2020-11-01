from pytest import fixture
from starlette.testclient import TestClient

from app.api import create_api
from app.core.services import JWTService
from app.settings import get_settings


@fixture
def jwt_service(settings_with_rsa):
    return JWTService(settings_with_rsa)


@fixture
def client(settings_with_rsa):
    api = create_api(settings_with_rsa)
    api.dependency_overrides[get_settings] = lambda: settings_with_rsa
    client = TestClient(api)
    return client

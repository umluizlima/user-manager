from pytest import fixture
from starlette.testclient import TestClient

from app.api import create_api
from app.core.repositories import UsersRepository
from app.core.services import JWTService
from app.settings import get_settings


@fixture
def settings(rsa_keys, settings):
    settings.JWT_PRIVATE_KEY = rsa_keys["private"]
    settings.JWT_PUBLIC_KEY = rsa_keys["public"]
    return settings


@fixture
def users_repository(db_session):
    return UsersRepository(db_session)


@fixture
def jwt_service(settings):
    return JWTService(settings)


@fixture
def client(settings):
    api = create_api(settings)
    api.dependency_overrides[get_settings] = lambda: settings
    client = TestClient(api)
    return client

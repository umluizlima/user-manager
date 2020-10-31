from unittest.mock import MagicMock

from pytest import fixture
from starlette.testclient import TestClient

from app.api import create_api
from app.api.dependencies import (
    code_service,
    get_jwt,
    jwt_service,
    send_code_producer,
    users_repository,
)

mock = MagicMock()


def get_mock():
    mock.reset_mock()
    return mock


@fixture
def mock_repository():
    return get_mock()


@fixture
def mock_dependency():
    return get_mock()


@fixture
def client(settings):
    api = create_api(settings)
    api.dependency_overrides[code_service] = get_mock
    api.dependency_overrides[jwt_service] = get_mock
    api.dependency_overrides[send_code_producer] = get_mock
    api.dependency_overrides[get_jwt] = get_mock
    api.dependency_overrides[users_repository] = get_mock
    client = TestClient(api)
    return client

from unittest.mock import MagicMock

from pytest import fixture
from starlette.testclient import TestClient

from app.api import create_api
from app.api.dependencies import token_checker, users_repository

mock = MagicMock()


def get_mock():
    mock.reset_mock()
    return mock


@fixture
def mock_repository():
    return get_mock()


@fixture
def client(settings):
    api = create_api(settings)
    api.dependency_overrides[users_repository] = get_mock
    api.dependency_overrides[token_checker] = get_mock
    client = TestClient(api)
    return client

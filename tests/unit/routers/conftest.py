from unittest.mock import MagicMock

from pytest import fixture
from starlette.testclient import TestClient

from app.api import create_api
from app.core.database import get_db


def mock_get_db():
    return MagicMock()


@fixture
def client(settings):
    api = create_api(settings)
    api.dependency_overrides[get_db] = mock_get_db
    client = TestClient(api)
    return client

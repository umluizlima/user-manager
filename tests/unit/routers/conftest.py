from pytest import fixture
from starlette.testclient import TestClient

from app.api import api


@fixture
def client():
    client = TestClient(api)
    return client

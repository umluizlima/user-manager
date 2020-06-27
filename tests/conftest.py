from os import environ

from pytest import fixture

from app.settings import Settings


@fixture(scope="session", autouse=True)
def environment():
    ...


@fixture
def settings():
    return get_test_settings()


def get_test_settings():
    return Settings(_env_file=None)

from pytest import fixture

from app.settings import Settings


@fixture
def settings():
    return Settings(_env_file=None)

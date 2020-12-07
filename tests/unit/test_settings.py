from pydantic import ValidationError
from pytest import raises

from app.settings import Environment
from tests.conftest import get_test_settings


def test_env_is_set_from_env(monkeypatch):
    expected = Environment.PRODUCTION.value
    monkeypatch.setenv("ENV", expected)
    assert get_test_settings().ENV == expected


def test_env_must_exist(monkeypatch):
    expected = "some-env-that-is-not-mapped"
    monkeypatch.setenv("ENV", expected)
    with raises(ValidationError):
        get_test_settings()


def test_env_has_default_value(monkeypatch):
    monkeypatch.delenv("ENV", raising=False)
    assert isinstance(get_test_settings().ENV, Environment)

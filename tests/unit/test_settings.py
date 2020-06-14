from pydantic import ValidationError
from pytest import raises

from app.settings import Environment, Settings


def test_api_key_is_set_from_env(monkeypatch):
    expected = "this_is_an_api_key"
    monkeypatch.setenv("API_KEY", expected)
    assert Settings(_env_file=None).API_KEY == expected


def test_api_key_has_default_value(monkeypatch):
    monkeypatch.delenv("API_KEY", raising=False)
    assert isinstance(Settings(_env_file=None).API_KEY, str)


def test_env_is_set_from_env(monkeypatch):
    expected = Environment.PRODUCTION.value
    monkeypatch.setenv("ENV", expected)
    assert Settings(_env_file=None).ENV == expected


def test_env_must_exist(monkeypatch):
    expected = "some-env-that-is-not-mapped"
    monkeypatch.setenv("ENV", expected)
    with raises(ValidationError):
        Settings(_env_file=None)


def test_env_has_default_value(monkeypatch):
    monkeypatch.delenv("ENV", raising=False)
    assert isinstance(Settings(_env_file=None).ENV, Environment)
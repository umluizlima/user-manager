from time import time

from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from pytest import fixture, raises

from app.core.services import JWTService


@fixture
def jwt_service(rsa_keys, settings):
    settings.JWT_PRIVATE_KEY = rsa_keys["private"]
    settings.JWT_PUBLIC_KEY = rsa_keys["public"]
    return JWTService(settings)


@fixture
def jwt_token(jwt_service):
    return jwt_service.generate_token({})


def test_jwt_service(jwt_service):
    jwt_service.generate_token({})


def test_generate_token_raises_exception_on_invalid_private_key(settings):
    jwt_service = JWTService(settings)
    with raises(ValueError):
        jwt_service.generate_token({})


def test_generate_token_raises_exception_on_invalid_claims(jwt_service):
    with raises(TypeError):
        jwt_service.generate_token(123)


def test_verify_token_raises_exception_on_invalid_public_key(jwt_token, settings):
    settings.JWT_PUBLIC_KEY = b""
    jwt_service = JWTService(settings)
    with raises(ValueError):
        jwt_service.verify_token(jwt_token)


def test_verify_token_raises_exception_on_tampered(jwt_service, jwt_token):
    jwt_token = jwt_token + "a"
    with raises(InvalidSignatureError):
        jwt_service.verify_token(jwt_token)


def test_verify_token_raises_exception_on_expired(jwt_service):
    jwt_token = jwt_service.generate_token({"exp": 0})
    with raises(ExpiredSignatureError):
        jwt_service.verify_token(jwt_token)


def test_verify_token_returns_claims(jwt_service):
    payload = {"test": 123}
    jwt_token = jwt_service.generate_token(payload)
    assert jwt_service.verify_token(jwt_token) == payload


def test_verify_token_returns_not_expired(jwt_service):
    payload = {"exp": time() + 100}
    jwt_token = jwt_service.generate_token(payload)
    assert jwt_service.verify_token(jwt_token) == payload

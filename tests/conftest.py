from os import environ

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from pytest import fixture

from app.settings import Settings


@fixture
def rsa_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return {"public": public_pem, "private": private_pem}


@fixture(scope="session", autouse=True)
def environment():
    environ["JWT_PUBLIC_KEY"] = "public-key"
    environ["JWT_PRIVATE_KEY"] = "private-key"


@fixture
def settings():
    return get_test_settings()


def get_test_settings():
    return Settings(_env_file=None)

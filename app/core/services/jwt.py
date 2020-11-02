from abc import ABC, abstractmethod
from time import time

from jwt import decode, encode

from app.core.schemas import AccessTokenPayload, BaseJWTPayload
from app.settings import Settings


class BaseJWTService(ABC):
    @property
    @abstractmethod
    def __payload__(self) -> BaseJWTPayload:
        ...

    def __init__(self, settings: Settings):
        self._settings = settings

    def generate_token(self, payload: BaseJWTPayload) -> str:
        if payload.exp is None:
            payload.exp = time() + self._settings.JWT_EXPIRATION_SECONDS
        return encode(
            payload=payload.dict(by_alias=True),
            key=self._settings.JWT_PRIVATE_KEY,
            algorithm=self._settings.JWT_ALGORITHM,
        ).decode(encoding="utf-8")

    def verify_token(self, token: str) -> BaseJWTPayload:
        return self.__payload__(
            **decode(
                jwt=token,
                key=self._settings.JWT_PUBLIC_KEY,
                algorithms=[self._settings.JWT_ALGORITHM],
            )
        )


class AccessTokenService(BaseJWTService):
    __payload__ = AccessTokenPayload

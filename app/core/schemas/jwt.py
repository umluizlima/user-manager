from enum import Enum
from time import time
from typing import List
from uuid import uuid4

from pydantic import BaseModel, Field

from app.core.models import User, UserRoles


def uuid_str() -> str:
    return str(uuid4())


def time_int() -> int:
    return int(time())


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class BaseJWTPayload(BaseModel):
    exp: int
    jti: str = Field(default_factory=uuid_str)
    nbf: int = Field(default_factory=time_int)
    token_type: TokenType

    @staticmethod
    def calc_exp(seconds_from_now: int = 0) -> int:
        return int(time()) + seconds_from_now


class AccessTokenPayload(BaseJWTPayload):
    roles: List[UserRoles]
    sid: str
    token_type: TokenType = TokenType.ACCESS
    user_id: int

    @staticmethod
    def from_info(expiration_seconds: int, session_id: str, user: User):
        return AccessTokenPayload(
            exp=AccessTokenPayload.calc_exp(expiration_seconds),
            roles=user.roles,
            sid=session_id,
            user_id=user.id,
        )


class RefreshTokenPayload(BaseJWTPayload):
    jti = str
    token_type: TokenType = TokenType.REFRESH

    @staticmethod
    def from_info(expiration_seconds: int, session_id: str):
        return RefreshTokenPayload(
            exp=RefreshTokenPayload.calc_exp(expiration_seconds), jti=session_id,
        )

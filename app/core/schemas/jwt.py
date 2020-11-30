from enum import Enum
from time import time
from typing import List
from uuid import uuid4

from pydantic import BaseModel

from app.core.models import UserRoles


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class BaseJWTPayload(BaseModel):
    exp: int
    jti: str = str(uuid4())
    nbf: int = int(time())
    token_type: TokenType

    @staticmethod
    def calc_exp(seconds_from_now: int = 0) -> int:
        return int(time()) + seconds_from_now


class AccessTokenPayload(BaseJWTPayload):
    roles: List[UserRoles]
    token_type: TokenType = TokenType.ACCESS
    user_id: int


class RefreshTokenPayload(BaseJWTPayload):
    jti = str
    token_type: TokenType = TokenType.REFRESH

from time import time
from typing import List
from uuid import uuid4

from pydantic import BaseModel

from app.core.models import UserRoles


class JWTPayload(BaseModel):
    exp: float
    jti: str = str(uuid4())
    nbf: float = time()
    roles: List[UserRoles]
    user_id: int

    @staticmethod
    def calc_exp(seconds_from_now: int = 0) -> float:
        return time() + seconds_from_now

from time import time
from typing import List, Optional
from uuid import uuid4

from pydantic import BaseModel

from app.core.models import UserRoles


class BaseJWTPayload(BaseModel):
    exp: Optional[float] = None
    jti: str = str(uuid4())
    nbf: float = time()


class AccessTokenPayload(BaseJWTPayload):
    user_id: int
    roles: List[UserRoles]

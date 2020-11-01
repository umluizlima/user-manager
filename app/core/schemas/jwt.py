from time import time
from typing import List, Optional
from uuid import uuid4

from pydantic import BaseModel

from app.core.models import UserRoles


class JWTPayload(BaseModel):
    exp: Optional[float] = None
    jti: str = str(uuid4())
    nbf: float = time()
    user_id: int
    roles: List[UserRoles]

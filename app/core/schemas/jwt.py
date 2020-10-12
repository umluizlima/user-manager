from time import time
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel


class JWTPayload(BaseModel):
    exp: Optional[float] = None
    jti: str = str(uuid4())
    nbf: float = time()
    user_id: int

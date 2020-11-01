from datetime import datetime
from typing import List

from pydantic import BaseModel, EmailStr

from app.core.models import UserRoles


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    ...


class UserUpdate(UserBase):
    email: EmailStr = None


class UserRead(UserBase):
    id: int
    created_at: datetime
    roles: List[UserRoles]

    class Config:
        orm_mode = True

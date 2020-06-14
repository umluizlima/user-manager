from datetime import datetime

from pydantic import BaseModel, constr, condecimal, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    ...


class UserUpdate(UserBase):
    ...


class UserRead(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

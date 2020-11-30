from pydantic import BaseModel, EmailStr


class AccessCodeCreate(BaseModel):
    email: EmailStr
    create_user: bool = False


class RefreshTokenCreate(BaseModel):
    email: EmailStr
    code: str


class AccessToken(BaseModel):
    access_token: str
    token_type: str = "bearer"

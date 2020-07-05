from pydantic import BaseModel, EmailStr


class TokenCreate(BaseModel):
    email: EmailStr
    create_user: bool = False


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

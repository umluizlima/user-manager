from sqlalchemy import Column, Text

from .base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    email = Column(Text, nullable=False, unique=True)

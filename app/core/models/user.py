from enum import Enum, auto

from sqlalchemy import Column, Text
from sqlalchemy.types import ARRAY

from .base import BaseModel


class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class UserRoles(str, AutoName):
    ADMIN = auto()


class User(BaseModel):
    __tablename__ = "users"

    email = Column(Text, nullable=False, unique=True)
    roles = Column(ARRAY(Text, dimensions=1), default=[])

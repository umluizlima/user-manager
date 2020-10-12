from enum import Enum
from typing import Dict

from pydantic import BaseModel, EmailStr, Field


class Transactional(str, Enum):
    ACCESS_CODE = "ACCESS_CODE"


class TransactionalSchema(BaseModel):
    transactional_type: Transactional = Field(alias="type")
    transactional_data: Dict = Field({}, alias="data")
    to_email: EmailStr = Field(alias="to")

    class Config:
        use_enum_values = True

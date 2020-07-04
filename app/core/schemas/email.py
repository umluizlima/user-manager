from typing import Optional

from pydantic import BaseModel, constr, EmailStr


class EmailSchema(BaseModel):
    to: EmailStr
    subject: constr(max_length=78)
    content: str
    content_type: str = "text/html"

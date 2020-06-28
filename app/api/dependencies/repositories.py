from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.repositories import UsersRepository


def users_repository(db: Session = Depends(get_db)):
    return UsersRepository(db)

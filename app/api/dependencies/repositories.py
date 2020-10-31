from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import Database
from app.core.repositories import UsersRepository
from app.settings import Settings, get_settings


def db_session(settings: Settings = Depends(get_settings)):
    db = Database(settings)
    with db.get_session() as session:
        yield session


def users_repository(db: Session = Depends(db_session)):
    return UsersRepository(db)

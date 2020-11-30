from typing import Dict

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import Database
from app.core.errors import ResourceAlreadyExistsError, ResourceNotFoundError
from app.core.models import User
from app.core.repositories import UsersRepository
from app.settings import Settings, get_settings

from .errors import raise_conflict, raise_not_found


def raise_user_not_found():
    raise_not_found("User not found")


def db_session(settings: Settings = Depends(get_settings)):
    db = Database(settings)
    with db.get_session() as session:
        yield session


def users_repository(db: Session = Depends(db_session)) -> UsersRepository:
    return UsersRepository(db)


def find_user_by_id(user_id: int, users_repository: UsersRepository) -> User:
    try:
        return users_repository.find_by_id(user_id)
    except ResourceNotFoundError:
        raise_user_not_found()


def update_user_by_id(
    user_id: int, user: Dict, users_repository: UsersRepository
) -> User:
    try:
        return users_repository.update_by_id(user_id, user)
    except ResourceNotFoundError:
        raise_user_not_found()
    except ResourceAlreadyExistsError:
        raise_conflict("User with data already exists")


def delete_user_by_id(user_id: int, users_repository: UsersRepository):
    try:
        return users_repository.delete_by_id(user_id)
    except ResourceNotFoundError:
        raise_user_not_found()

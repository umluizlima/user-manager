from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

from app.core.database import Database
from app.core.errors import ResourceAlreadyExistsError, ResourceNotFoundError
from app.core.models import User
from app.core.repositories import UsersRepository
from app.core.schemas import UserUpdate
from app.settings import Settings, get_settings


def db_session(settings: Settings = Depends(get_settings)):
    db = Database(settings)
    with db.get_session() as session:
        yield session


def users_repository(db: Session = Depends(db_session)) -> UsersRepository:
    return UsersRepository(db)


def find_user_by_id(user_id: int, users: UsersRepository) -> User:
    try:
        return users.find_by_id(user_id)
    except ResourceNotFoundError:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")


def update_user_by_id(user_id: int, user: UserUpdate, users: UsersRepository) -> User:
    try:
        return users.update_by_id(user_id, user.dict(exclude_unset=True))
    except ResourceNotFoundError:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")
    except ResourceAlreadyExistsError:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT, detail="User with data already exists"
        )


def delete_user_by_id(user_id: int, users: UsersRepository):
    try:
        return users.delete_by_id(user_id)
    except ResourceNotFoundError:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")

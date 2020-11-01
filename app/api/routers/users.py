from typing import List

from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_409_CONFLICT

from app.core.errors import ResourceAlreadyExistsError
from app.core.repositories import UsersRepository
from app.core.schemas import UserCreate, UserRead, UserUpdate

from ..dependencies import (
    delete_user_by_id,
    find_user_by_id,
    get_jwt,
    update_user_by_id,
    users_repository,
)

router = APIRouter()


@router.post("/users", response_model=UserRead, status_code=HTTP_201_CREATED)
def create(user: UserCreate, users: UsersRepository = Depends(users_repository)):
    try:
        return users.create(user.dict())
    except ResourceAlreadyExistsError:
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail="User already exists")


@router.get("/users", response_model=List[UserRead])
def list(users: UsersRepository = Depends(users_repository)):
    return users.find_all()


@router.get("/users/{user_id}", response_model=UserRead)
def read(user_id: int, users: UsersRepository = Depends(users_repository)):
    return find_user_by_id(user_id, users)


@router.put("/users/{user_id}", response_model=UserRead)
def update(
    user_id: int, user: UserUpdate, users: UsersRepository = Depends(users_repository)
):
    return update_user_by_id(user_id, user, users)


@router.delete("/users/{user_id}", status_code=HTTP_204_NO_CONTENT)
def delete(user_id: int, users: UsersRepository = Depends(users_repository)):
    return delete_user_by_id(user_id, users)


def configure(app, settings):
    app.include_router(
        router, tags=["users"], prefix="/api/v1", dependencies=[Depends(get_jwt)],
    )

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)

from app.core.errors import ResourceAlreadyExistsError, ResourceNotFoundError
from app.core.repositories import UsersRepository
from app.core.schemas import UserCreate, UserRead, UserUpdate

from ..dependencies import token_checker, users_repository

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
    try:
        return users.find_by_id(user_id)
    except ResourceNotFoundError:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")


@router.put("/users/{user_id}", response_model=UserRead)
def update(
    user_id: int, user: UserUpdate, users: UsersRepository = Depends(users_repository)
):
    try:
        return users.update_by_id(user_id, user.dict(exclude_unset=True))
    except ResourceNotFoundError:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")
    except ResourceAlreadyExistsError:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT, detail="User with data already exists"
        )


@router.delete("/users/{user_id}", status_code=HTTP_204_NO_CONTENT)
def delete(user_id: int, users: UsersRepository = Depends(users_repository)):
    try:
        return users.delete_by_id(user_id)
    except ResourceNotFoundError:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")


def configure(app, settings):
    app.include_router(
        router, tags=["users"], prefix="/api/v1", dependencies=[Depends(token_checker)],
    )

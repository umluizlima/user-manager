from typing import List

from fastapi import APIRouter, Depends
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT

from app.core.errors import ResourceAlreadyExistsError
from app.core.models import UserRoles
from app.core.repositories import UsersRepository
from app.core.schemas import UserCreate, UserRead, UserUpdate

from ..dependencies import (
    WithRoles,
    delete_user_by_id,
    find_user_by_id,
    raise_conflict,
    update_user_by_id,
    users_repository,
)

router = APIRouter()


@router.post("/users", response_model=UserRead, status_code=HTTP_201_CREATED)
def create_user(
    user: UserCreate, users_repository: UsersRepository = Depends(users_repository)
):
    try:
        return users_repository.create(user.dict())
    except ResourceAlreadyExistsError:
        raise_conflict("User already exists")


@router.get("/users", response_model=List[UserRead])
def list_users(users_repository: UsersRepository = Depends(users_repository)):
    return users_repository.find_all()


@router.get("/users/{user_id}", response_model=UserRead)
def read_user(
    user_id: int, users_repository: UsersRepository = Depends(users_repository)
):
    return find_user_by_id(user_id, users_repository)


@router.put("/users/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    user: UserUpdate,
    users_repository: UsersRepository = Depends(users_repository),
):
    return update_user_by_id(user_id, user.dict(exclude_unset=True), users_repository)


@router.delete("/users/{user_id}", status_code=HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int, users_repository: UsersRepository = Depends(users_repository)
):
    return delete_user_by_id(user_id, users_repository)


def configure(app, settings):
    app.include_router(
        router,
        tags=["users"],
        prefix="/api/v1",
        dependencies=[Depends(WithRoles([UserRoles.ADMIN]))],
    )

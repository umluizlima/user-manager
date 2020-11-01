from fastapi import APIRouter, Depends
from starlette.status import HTTP_204_NO_CONTENT

from app.core.models import User
from app.core.repositories import UsersRepository
from app.core.schemas import JWTPayload, UserRead, UserUpdate

from ..dependencies import (
    delete_user_by_id,
    get_current_user,
    get_jwt,
    update_user_by_id,
    users_repository,
)

router = APIRouter()


@router.get("/users/me", response_model=UserRead)
def read_self(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/users/me", response_model=UserRead)
def update_self(
    user: UserUpdate,
    jwt: JWTPayload = Depends(get_jwt),
    users_repository: UsersRepository = Depends(users_repository),
):
    return update_user_by_id(jwt.user_id, user, users_repository)


@router.delete("/users/me", status_code=HTTP_204_NO_CONTENT)
def delete_self(
    jwt: JWTPayload = Depends(get_jwt),
    users_repository: UsersRepository = Depends(users_repository),
):
    return delete_user_by_id(jwt.user_id, users_repository)


def configure(app, settings):
    app.include_router(
        router, tags=["current user"], prefix="/api/v1",
    )

from fastapi import APIRouter, Depends
from starlette.status import HTTP_204_NO_CONTENT

from app.core.models import User
from app.core.repositories import UsersRepository
from app.core.schemas import AccessTokenPayload, UserRead, UserUpdate

from ..dependencies import (
    access_token,
    current_user,
    delete_user_by_id,
    update_user_by_id,
    users_repository,
)

router = APIRouter()


@router.get("/users/me", response_model=UserRead)
def read_self(current_user: User = Depends(current_user)):
    return current_user


@router.put("/users/me", response_model=UserRead)
def update_self(
    user: UserUpdate,
    jwt: AccessTokenPayload = Depends(access_token),
    users_repository: UsersRepository = Depends(users_repository),
):
    return update_user_by_id(
        jwt.user_id, user.dict(exclude_unset=True), users_repository
    )


@router.delete("/users/me", status_code=HTTP_204_NO_CONTENT)
def delete_self(
    jwt: AccessTokenPayload = Depends(access_token),
    users_repository: UsersRepository = Depends(users_repository),
):
    return delete_user_by_id(jwt.user_id, users_repository)


def configure(app, settings):
    app.include_router(
        router, tags=["current user"], prefix="/api/v1",
    )

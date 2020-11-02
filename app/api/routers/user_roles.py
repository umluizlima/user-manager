from typing import List

from fastapi import APIRouter, Depends

from app.core.models import UserRoles
from app.core.repositories import UsersRepository
from app.core.schemas import UserRead

from ..dependencies import WithRoles, update_user_by_id, users_repository

router = APIRouter()


@router.put("/users/{user_id}/roles", response_model=UserRead)
def update_user_roles(
    user_id: int,
    user_roles: List[UserRoles],
    users_repository: UsersRepository = Depends(users_repository),
):
    return update_user_by_id(user_id, {"roles": user_roles}, users_repository)


def configure(app, settings):
    app.include_router(
        router,
        tags=["user roles"],
        prefix="/api/v1",
        dependencies=[Depends(WithRoles([UserRoles.ADMIN]))],
    )

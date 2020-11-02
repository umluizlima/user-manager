from typing import List

from fastapi import APIRouter, Depends

from app.core.models import UserRoles
from app.core.repositories import UsersRepository
from app.core.schemas import UserRead

from ..dependencies import WithRoles, users_repository

router = APIRouter()


@router.put("/users/{user_id}/roles", response_model=UserRead)
def update_user_roles(
    user_id: int,
    user_roles: List[UserRoles],
    users_repository: UsersRepository = Depends(users_repository),
):
    return users_repository.update_by_id(user_id, {"roles": user_roles})


def configure(app, settings):
    app.include_router(
        router,
        tags=["user roles"],
        prefix="/api/v1",
        dependencies=[Depends(WithRoles([UserRoles.ADMIN]))],
    )

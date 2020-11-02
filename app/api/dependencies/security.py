import logging
from typing import List

from fastapi import Depends, HTTPException, Security
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer
from starlette.status import HTTP_403_FORBIDDEN

from app.core.models import User, UserRoles
from app.core.repositories import UsersRepository
from app.core.schemas import AccessTokenPayload
from app.core.services import AccessTokenService
from app.settings import Settings, get_settings

from .repositories import find_user_by_id, users_repository

jwt_scheme = HTTPBearer(scheme_name="JWT")


def access_token_service(
    settings: Settings = Depends(get_settings),
) -> AccessTokenService:
    return AccessTokenService(settings)


def get_jwt(
    access_token_service: AccessTokenService = Depends(access_token_service),
    header: HTTPAuthorizationCredentials = Security(jwt_scheme),
) -> AccessTokenPayload:
    try:
        return access_token_service.verify_token(header.credentials)
    except Exception:
        logging.exception("Token verification raised exception")
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )


def get_current_user(
    jwt: AccessTokenPayload = Depends(get_jwt),
    users_repository: UsersRepository = Depends(users_repository),
) -> User:
    return find_user_by_id(jwt.user_id, users_repository)


class WithRoles:
    def __init__(self, roles: List[UserRoles]):
        self._roles = set(roles)

    def __call__(self, jwt: AccessTokenPayload = Depends(get_jwt)):
        if not self._roles.intersection(jwt.roles):
            role_values = [role.value for role in self._roles]
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail=f"User lacks required roles: {role_values}",
            )

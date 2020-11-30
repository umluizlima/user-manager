from typing import List

from fastapi import Depends, Security
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer

from app.core.models import User, UserRoles
from app.core.repositories import UsersRepository
from app.core.schemas import AccessTokenPayload, RefreshTokenCreate
from app.core.services import AccessCodeService, JWTService

from .errors import raise_forbidden, raise_unauthorized
from .repositories import find_user_by_email, find_user_by_id, users_repository
from .services import access_code_service, jwt_service

jwt_scheme = HTTPBearer(scheme_name="JWT")


def authorization_bearer_token(
    header: HTTPAuthorizationCredentials = Security(jwt_scheme),
) -> str:
    return header.credentials


def access_code_user(
    body: RefreshTokenCreate,
    access_code_service: AccessCodeService = Depends(access_code_service),
    users_repository: UsersRepository = Depends(users_repository),
) -> User:
    user = find_user_by_email(body.email, users_repository)
    if not access_code_service.verify_code(user.id, body.code):
        raise_unauthorized("Invalid access code")
    return user


def access_token(
    jwt_service: JWTService = Depends(jwt_service),
    token: str = Depends(authorization_bearer_token),
) -> AccessTokenPayload:
    try:
        return AccessTokenPayload(**jwt_service.verify_token(token))
    except Exception:
        raise_unauthorized("Invalid access token")


def current_user(
    access_token: AccessTokenPayload = Depends(access_token),
    users_repository: UsersRepository = Depends(users_repository),
) -> User:
    return find_user_by_id(access_token.user_id, users_repository)


class WithRoles:
    def __init__(self, roles: List[UserRoles]):
        self._roles = set(roles)

    def __call__(self, access_token: AccessTokenPayload = Depends(access_token)):
        if not self._roles.intersection(access_token.roles):
            role_values = [role.value for role in self._roles]
            raise_forbidden(f"User lacks required roles: {role_values}")

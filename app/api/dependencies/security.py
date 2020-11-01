import logging

from fastapi import Depends, HTTPException, Security
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer
from starlette.status import HTTP_403_FORBIDDEN

from app.core.models import User
from app.core.repositories import UsersRepository
from app.core.schemas import JWTPayload
from app.core.services import JWTService
from app.settings import Settings, get_settings

from .repositories import find_user_by_id, users_repository

jwt_scheme = HTTPBearer(scheme_name="JWT")


def jwt_service(settings: Settings = Depends(get_settings)):
    return JWTService(settings)


def get_jwt(
    jwt_service: JWTService = Depends(jwt_service),
    header: HTTPAuthorizationCredentials = Security(jwt_scheme),
) -> JWTPayload:
    try:
        return jwt_service.verify_token(header.credentials)
    except Exception:
        logging.exception("Token verification raised exception")
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )


def get_current_user(
    jwt: JWTPayload = Depends(get_jwt),
    users_repository: UsersRepository = Depends(users_repository),
) -> User:
    return find_user_by_id(jwt.user_id, users_repository)

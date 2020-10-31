import logging

from fastapi import Depends, HTTPException, Security
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer
from starlette.status import HTTP_403_FORBIDDEN

from app.core.schemas import JWTPayload
from app.core.services import JWTService
from app.settings import Settings, get_settings

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

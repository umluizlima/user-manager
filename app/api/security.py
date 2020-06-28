import logging

from fastapi import Depends, Security, HTTPException
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer
from starlette.status import HTTP_403_FORBIDDEN

from app.core.services import JWTService
from app.settings import get_settings, Settings

jwt_scheme = HTTPBearer(scheme_name="JWT")


def jwt_service(settings: Settings = Depends(get_settings)):
    return JWTService(settings)


def token_checker(
    token_service: JWTService = Depends(jwt_service),
    header: HTTPAuthorizationCredentials = Security(jwt_scheme),
):
    try:
        return token_service.verify_token(header.credentials)
    except Exception:
        logging.exception("Token verification raised exception")
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )

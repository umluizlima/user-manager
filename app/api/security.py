from fastapi import Depends, Security, HTTPException
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer
from starlette.status import HTTP_403_FORBIDDEN

from app.core.services import JWTService
from app.settings import get_settings, Settings


def jwt_service(settings: Settings = Depends(get_settings)):
    return JWTService(settings)


class TokenChecker:
    _scheme = HTTPBearer(scheme_name="JWT")

    def __init__(self, token_service: JWTService = Depends(jwt_service)):
        self._token_service = token_service

    def __call__(self, header: HTTPAuthorizationCredentials = Security(_scheme)):
        try:
            return self._token_service.verify_token(header.credentials)
        except Exception:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
            )


token_checker = TokenChecker()

from fastapi import Security, HTTPException
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer
from starlette.status import HTTP_403_FORBIDDEN

from app.core.services import JWTService


class TokenChecker:
    scheme = HTTPBearer(scheme_name="JWT")

    def __init__(self, token_service: JWTService = JWTService()):
        self.token_service = token_service

    def __call__(self, header: HTTPAuthorizationCredentials = Security(scheme)):
        try:
            return self.token_service.verify_token(header.credentials)
        except Exception:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
            )


token_checker = TokenChecker()

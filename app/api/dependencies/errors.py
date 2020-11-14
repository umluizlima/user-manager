from fastapi.exceptions import HTTPException
from starlette.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)


def raise_http_exception(status_code: int, detail: str):
    raise HTTPException(status_code, detail)


def raise_unauthorized(detail: str):
    raise_http_exception(HTTP_401_UNAUTHORIZED, detail)


def raise_forbidden(detail: str):
    raise_http_exception(HTTP_403_FORBIDDEN, detail)


def raise_not_found(detail: str):
    raise_http_exception(HTTP_404_NOT_FOUND, detail)


def raise_conflict(detail: str):
    raise_http_exception(HTTP_409_CONFLICT, detail)

from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from app.core.errors import ResourceNotFoundError
from app.core.repositories import UsersRepository
from app.core.schemas import (
    AccessCodeCreate,
    AccessToken,
    AccessTokenCreate,
    AccessTokenPayload,
    UserCreate,
)
from app.core.services import AccessTokenService, CodeService
from app.core.tasks import SendCodeProducer

from ..dependencies import (
    access_token_service,
    code_service,
    send_code_producer,
    users_repository,
)

router = APIRouter()


@router.post("/authentication/access-code", status_code=HTTP_202_ACCEPTED)
def generate_access_code(
    body: AccessCodeCreate,
    users: UsersRepository = Depends(users_repository),
    code_service: CodeService = Depends(code_service),
    producer: SendCodeProducer = Depends(send_code_producer),
):
    user = None
    try:
        user = users.find_by_email(body.email)
    except ResourceNotFoundError:
        if body.create_user:
            user = users.create(UserCreate(email=body.email).dict())
    if not user:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="User not registered"
        )
    code = code_service.generate_code(f"access_code:{user.id}")
    producer.send_code(code, user.email)


@router.post(
    "/authentication/access-token",
    response_model=AccessToken,
    status_code=HTTP_202_ACCEPTED,
)
def generate_access_token(
    body: AccessTokenCreate,
    users: UsersRepository = Depends(users_repository),
    code_service: CodeService = Depends(code_service),
    access_token_service: AccessTokenService = Depends(access_token_service),
):
    user = None
    try:
        user = users.find_by_email(body.email)
    except ResourceNotFoundError:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="User not registered"
        )
    if not code_service.verify_code(f"access_code:{user.id}", body.code):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Invalid access code"
        )
    jwt = access_token_service.generate_token(
        AccessTokenPayload(user_id=user.id, roles=user.roles)
    )
    return AccessToken(access_token=jwt)


def configure(app, settings):
    app.include_router(
        router, tags=["authentication"], prefix="/api/v1",
    )

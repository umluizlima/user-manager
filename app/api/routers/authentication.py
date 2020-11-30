from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_202_ACCEPTED

from app.core.errors import ResourceNotFoundError
from app.core.repositories import UsersRepository
from app.core.schemas import (
    AccessCodeCreate,
    AccessToken,
    AccessTokenPayload,
    RefreshTokenCreate,
    UserCreate,
)
from app.core.services import AccessCodeService, JWTService
from app.core.tasks import SendCodeProducer
from app.settings import Settings, get_settings

from ..dependencies import (
    access_code_service,
    find_user_by_email,
    jwt_service,
    raise_bad_request,
    raise_not_found,
    send_code_producer,
    users_repository,
)

router = APIRouter()


@router.post("/authentication/code", status_code=HTTP_201_CREATED)
def generate_access_code(
    body: AccessCodeCreate,
    access_code_service: AccessCodeService = Depends(access_code_service),
    producer: SendCodeProducer = Depends(send_code_producer),
    users_repository: UsersRepository = Depends(users_repository),
):
    try:
        user = find_user_by_email(body.email, users_repository)
    except HTTPException as error:
        if not body.create_user:
            raise error
        user = users_repository.create(UserCreate(email=body.email).dict())
    code = access_code_service.generate_code(user.id)
    producer.send_code(code, user.email)


@router.post(
    "/authentication/access-token",
    response_model=AccessToken,
    status_code=HTTP_202_ACCEPTED,
)
def generate_access_token(
    body: RefreshTokenCreate,
    settings: Settings = Depends(get_settings),
    users: UsersRepository = Depends(users_repository),
    access_code_service: AccessCodeService = Depends(access_code_service),
    jwt_service: JWTService = Depends(jwt_service),
):
    user = None
    try:
        user = users.find_by_email(body.email)
    except ResourceNotFoundError:
        raise_not_found("User not registered")
    if not access_code_service.verify_code(user.id, body.code):
        raise_bad_request("Invalid access code")
    jwt_payload = AccessTokenPayload(
        user_id=user.id,
        roles=user.roles,
        exp=AccessTokenPayload.calc_exp(settings.ACCESS_TOKEN_EXPIRATION_SECONDS),
    )
    jwt = jwt_service.generate_token(jwt_payload.dict())
    return AccessToken(access_token=jwt)


def configure(app, settings):
    app.include_router(
        router, tags=["authentication"], prefix="/api/v1",
    )

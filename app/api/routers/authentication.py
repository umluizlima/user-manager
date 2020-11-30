from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_201_CREATED

from app.core.models import User
from app.core.repositories import UsersRepository
from app.core.schemas import (
    AccessCodeCreate,
    AccessToken,
    AccessTokenPayload,
    UserCreate,
)
from app.core.services import AccessCodeService, JWTService
from app.core.tasks import SendCodeProducer
from app.settings import Settings, get_settings

from ..dependencies import (
    access_code_service,
    access_code_user,
    find_user_by_email,
    jwt_service,
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
    "/authentication/token", response_model=AccessToken, status_code=HTTP_201_CREATED,
)
def generate_access_token(
    access_code_user: User = Depends(access_code_user),
    jwt_service: JWTService = Depends(jwt_service),
    settings: Settings = Depends(get_settings),
):
    payload = AccessTokenPayload(
        user_id=access_code_user.id,
        roles=access_code_user.roles,
        exp=AccessTokenPayload.calc_exp(settings.ACCESS_TOKEN_EXPIRATION_SECONDS),
    )
    token = jwt_service.generate_token(payload.dict())
    return AccessToken(access_token=token)


def configure(app, settings):
    app.include_router(
        router, tags=["authentication"], prefix="/api/v1",
    )

from fastapi import APIRouter, Depends, HTTPException, Response
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from app.core.models import User
from app.core.repositories import UsersRepository
from app.core.schemas import (
    AccessCodeCreate,
    AccessToken,
    AccessTokenPayload,
    RefreshTokenPayload,
    UserCreate,
)
from app.core.services import AccessCodeService, JWTService, SessionService
from app.core.tasks import SendCodeProducer
from app.settings import Settings, get_settings

from ..dependencies import (
    access_code_service,
    access_code_user,
    find_user_by_email,
    find_user_by_id,
    jwt_service,
    raise_unauthorized,
    refresh_token,
    send_code_producer,
    session_service,
    users_repository,
)

router = APIRouter()


@router.post("/authentication/code", status_code=HTTP_201_CREATED)
def send_access_code(
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
def create_user_session(
    response: Response,
    access_code_user: User = Depends(access_code_user),
    jwt_service: JWTService = Depends(jwt_service),
    session_service: SessionService = Depends(session_service),
    settings: Settings = Depends(get_settings),
):
    session_id = session_service.generate_session(access_code_user.id)
    refresh_token_payload = RefreshTokenPayload.from_info(
        settings.SESSION_EXPIRATION_SECONDS, session_id,
    )
    refresh_token = jwt_service.generate_token(refresh_token_payload.dict())
    access_token_payload = AccessTokenPayload.from_info(
        settings.ACCESS_TOKEN_EXPIRATION_SECONDS, session_id, access_code_user,
    )
    access_token = jwt_service.generate_token(access_token_payload.dict())
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        expires=settings.SESSION_EXPIRATION_SECONDS,
    )
    return AccessToken(access_token=access_token)


@router.get(
    "/authentication/token", response_model=AccessToken, status_code=HTTP_200_OK,
)
def get_fresh_token(
    jwt_service: JWTService = Depends(jwt_service),
    refresh_token: RefreshTokenPayload = Depends(refresh_token),
    session_service: SessionService = Depends(session_service),
    settings: Settings = Depends(get_settings),
    users_repository: UsersRepository = Depends(users_repository),
):
    user_id = session_service.verify_session(refresh_token.jti)
    if not user_id:
        raise_unauthorized("Invalid session")
    user = find_user_by_id(user_id, users_repository)
    payload = AccessTokenPayload.from_info(
        settings.ACCESS_TOKEN_EXPIRATION_SECONDS, refresh_token.jti, user,
    )
    token = jwt_service.generate_token(payload.dict())
    return AccessToken(access_token=token)


def configure(app, settings):
    app.include_router(
        router, tags=["authentication"], prefix="/api/v1",
    )

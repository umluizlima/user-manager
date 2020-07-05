import logging

from fastapi import APIRouter, Depends, HTTPException
from starlette.status import (
    HTTP_202_ACCEPTED,
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
)
from pydantic import EmailStr

from app.core.errors import ResourceAlreadyExistsError, ResourceNotFoundError
from app.core.repositories import UsersRepository
from app.core.schemas import TokenCreate, Token, UserCreate, UserRead
from app.core.services import CodeService, JWTService
from app.core.tasks import SendCodeProducer

from ..dependencies import (
    code_service,
    jwt_service,
    send_code_producer,
    token_checker,
    users_repository,
)

router = APIRouter()


@router.post("/authentication", status_code=HTTP_202_ACCEPTED)
def generate_code(
    body: TokenCreate,
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
    code = code_service.generate_code(f"user:{user.id}")
    producer.send_code(code, user.email)


@router.get("/authentication", response_model=Token)
def retrieve_token(
    email: EmailStr,
    code: str,
    users: UsersRepository = Depends(users_repository),
    code_service: CodeService = Depends(code_service),
    jwt_service: JWTService = Depends(jwt_service),
):
    user = None
    try:
        user = users.find_by_email(email)
    except ResourceNotFoundError:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="User not registered"
        )
    if not code_service.verify_code(f"user:{user.id}", code):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Invalid access code"
        )
    jwt = jwt_service.generate_token({"user_id": user.id})
    return Token(access_token=jwt)


def configure(app, settings):
    app.include_router(
        router, tags=["authentication"], prefix="/api/v1",
    )
from pytest import fixture
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
)

from app.core.schemas import (
    AccessCodeCreate,
    AccessToken,
    RefreshTokenCreate,
    RefreshTokenPayload,
)
from app.core.services import AccessCodeService

code = "123456"
access_code_body_1 = AccessCodeCreate(email="email@domain.com", create_user=False)
access_code_body_2 = AccessCodeCreate(email="anotheremail@domain.com", create_user=True)
access_token_body = RefreshTokenCreate(email="email@domain.com", code=code)


def send_access_code_request(client, payload):
    return client.post("/api/v1/authentication/code", json=payload)


def test_send_access_code_should_return_status_201(client, users_repository):
    users_repository.create({"email": access_code_body_1.email})
    response = send_access_code_request(client, access_code_body_1.dict())
    assert response.status_code == HTTP_201_CREATED


def test_send_access_code_should_return_status_404_if_user_is_not_found(client):
    response = send_access_code_request(client, access_code_body_1.dict())
    assert response.status_code == HTTP_404_NOT_FOUND


def test_send_access_code_should_create_user(client, users_repository):
    send_access_code_request(client, access_code_body_2.dict())
    assert len(users_repository.find_all()) == 1


def test_send_access_code_should_send_code_if_user_exists(
    client, send_code_producer_mock, users_repository, cache_client
):
    send_code_producer_mock.reset_mock()
    user = users_repository.create({"email": access_code_body_1.email})
    send_access_code_request(client, access_code_body_1.dict())
    send_code_producer_mock.send_code.assert_called_once_with(
        cache_client.get(AccessCodeService._get_access_code_key(user.id)).decode(
            "utf-8"
        ),
        user.email,
    )


def create_user_session_request(client, payload):
    return client.post("/api/v1/authentication/token", json=payload)


def test_create_user_session_should_return_status_201(
    client, cache_adapter, users_repository
):
    user = users_repository.create({"email": access_code_body_1.email})
    cache_adapter.set_with_expiration(
        AccessCodeService._get_access_code_key(user.id), 1, code
    )
    response = create_user_session_request(client, access_token_body.dict())
    assert response.status_code == HTTP_201_CREATED


def test_create_user_session_should_set_refresh_token_cookie(
    client, cache_adapter, users_repository
):
    user = users_repository.create({"email": access_code_body_1.email})
    cache_adapter.set_with_expiration(
        AccessCodeService._get_access_code_key(user.id), 1, code
    )
    response = create_user_session_request(client, access_token_body.dict())
    assert response.cookies.get("refresh_token")


def test_create_user_session_should_return_access_token(
    client, cache_adapter, users_repository
):
    user = users_repository.create({"email": access_code_body_1.email})
    cache_adapter.set_with_expiration(
        AccessCodeService._get_access_code_key(user.id), 1, code
    )
    response = create_user_session_request(client, access_token_body.dict())
    assert AccessToken(**response.json())


def test_create_user_session_should_return_status_404_if_user_not_found(client):
    response = create_user_session_request(client, access_token_body.dict())
    assert response.status_code == HTTP_404_NOT_FOUND


def test_create_user_session_should_return_status_401_if_code_is_invalid(
    client, users_repository
):
    users_repository.create({"email": access_code_body_1.email})
    response = create_user_session_request(client, access_token_body.dict())
    assert response.status_code == HTTP_401_UNAUTHORIZED


@fixture
def refresh_token(jwt_service, session_service, settings, users_repository):
    user = users_repository.create({"email": access_code_body_1.email})
    session_id = session_service.generate_session(user.id)
    refresh_token_payload = RefreshTokenPayload.from_info(
        settings.SESSION_EXPIRATION_SECONDS, session_id,
    )
    return jwt_service.generate_token(refresh_token_payload.dict())


def get_fresh_token_request(client, refresh_token):
    headers = {"Cookie": f"refresh_token={refresh_token}"} if refresh_token else {}
    return client.get("/api/v1/authentication/token", headers=headers,)


def test_get_fresh_token_should_return_status_200(client, refresh_token):
    response = get_fresh_token_request(client, refresh_token)
    assert response.status_code == HTTP_200_OK


def test_get_fresh_token_should_return_access_token(client, refresh_token):
    response = get_fresh_token_request(client, refresh_token)
    assert AccessToken(**response.json())


def test_get_fresh_token_should_return_unique_token(client, refresh_token):
    response_1 = get_fresh_token_request(client, refresh_token)
    token_1 = AccessToken(**response_1.json()).access_token
    response_2 = get_fresh_token_request(client, refresh_token)
    token_2 = AccessToken(**response_2.json()).access_token
    assert token_1 != token_2


def test_get_fresh_token_should_return_status_404_if_user_not_found(
    client, jwt_service, session_service, settings
):
    session_id = session_service.generate_session(123)
    refresh_token_payload = RefreshTokenPayload.from_info(
        settings.SESSION_EXPIRATION_SECONDS, session_id,
    )
    refresh_token = jwt_service.generate_token(refresh_token_payload.dict())

    response = get_fresh_token_request(client, refresh_token)
    assert response.status_code == HTTP_404_NOT_FOUND


def test_get_fresh_token_should_return_status_401_if_session_is_invalid(
    client, jwt_service, settings
):
    refresh_token_payload = RefreshTokenPayload.from_info(
        settings.SESSION_EXPIRATION_SECONDS, 123,
    )
    refresh_token = jwt_service.generate_token(refresh_token_payload.dict())

    response = get_fresh_token_request(client, refresh_token)
    assert response.status_code == HTTP_401_UNAUTHORIZED


def test_get_fresh_token_should_return_401_if_token_is_invalid(client):
    response = get_fresh_token_request(client, "invalid.token")
    assert response.status_code == HTTP_401_UNAUTHORIZED


def test_get_fresh_token_should_return_401_if_token_is_missing(client):
    response = get_fresh_token_request(client, None)
    assert response.status_code == HTTP_401_UNAUTHORIZED

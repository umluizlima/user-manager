from starlette.status import HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from app.core.schemas import AccessCodeCreate, AccessToken, AccessTokenCreate
from app.core.services import AccessCodeService

code = "123456"
access_code_body_1 = AccessCodeCreate(email="email@domain.com", create_user=False)
access_code_body_2 = AccessCodeCreate(email="anotheremail@domain.com", create_user=True)
access_token_body = AccessTokenCreate(email="email@domain.com", code=code)


def generate_access_code_request(client, payload):
    return client.post("/api/v1/authentication/access-code", json=payload)


def test_generate_access_code_should_return_status_202(client, users_repository):
    users_repository.create({"email": access_code_body_1.email})
    response = generate_access_code_request(client, access_code_body_1.dict())
    assert response.status_code == HTTP_202_ACCEPTED


def test_generate_access_code_should_return_status_404_if_user_is_not_found(client):
    response = generate_access_code_request(client, access_code_body_1.dict())
    assert response.status_code == HTTP_404_NOT_FOUND


def test_generate_access_code_should_create_user(client, users_repository):
    generate_access_code_request(client, access_code_body_2.dict())
    assert len(users_repository.find_all()) == 1


def test_generate_access_code_should_send_code_if_user_exists(
    client, send_code_producer_mock, users_repository, cache_client
):
    send_code_producer_mock.reset_mock()
    user = users_repository.create({"email": access_code_body_1.email})
    generate_access_code_request(client, access_code_body_1.dict())
    send_code_producer_mock.send_code.assert_called_once_with(
        cache_client.get(AccessCodeService._get_access_code_key(user.id)).decode(
            "utf-8"
        ),
        user.email,
    )


def generate_access_token_request(client, payload):
    return client.post("/api/v1/authentication/access-token", json=payload)


def test_generate_access_token_should_return_status_202(
    client, cache_adapter, users_repository
):
    user = users_repository.create({"email": access_code_body_1.email})
    cache_adapter.set_with_expiration(
        AccessCodeService._get_access_code_key(user.id), 1, code
    )
    response = generate_access_token_request(client, access_token_body.dict())
    assert response.status_code == HTTP_202_ACCEPTED


def test_generate_access_token_should_return_token(
    client, cache_adapter, users_repository
):
    user = users_repository.create({"email": access_code_body_1.email})
    cache_adapter.set_with_expiration(
        AccessCodeService._get_access_code_key(user.id), 1, code
    )
    response = generate_access_token_request(client, access_token_body.dict())
    assert AccessToken(**response.json())


def test_generate_access_token_should_return_status_404_if_user_not_found(client):
    response = generate_access_token_request(client, access_token_body.dict())
    assert response.status_code == HTTP_404_NOT_FOUND


def test_generate_access_token_should_return_status_400_if_code_is_invalid(
    client, users_repository
):
    users_repository.create({"email": access_code_body_1.email})
    response = generate_access_token_request(client, access_token_body.dict())
    assert response.status_code == HTTP_400_BAD_REQUEST

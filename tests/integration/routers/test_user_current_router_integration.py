from pytest import fixture
from starlette.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)

from app.core.schemas import AccessTokenPayload, UserRead

user_dict = {"email": "email@domain.com"}
update_payload = {"email": "new@email.com"}


@fixture
def user(users_repository):
    return users_repository.create(user_dict)


@fixture
def user_jwt(jwt_service, user):
    jwt_payload = AccessTokenPayload(
        user_id=user.id, roles=user.roles, exp=AccessTokenPayload.calc_exp(1)
    )
    return jwt_service.generate_token(jwt_payload.dict())


def read_self_request(client, jwt):
    return client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {jwt}"})


@fixture
def read_self_response(client, user_jwt):
    yield read_self_request(client, user_jwt)


def test_read_self_should_return_status_200_for_valid_jwt(read_self_response):
    assert read_self_response.status_code == HTTP_200_OK


def test_read_self_should_return_json(read_self_response):
    assert read_self_response.headers["Content-Type"] == "application/json"


def test_read_self_should_return_user_schema(read_self_response):
    assert UserRead(**read_self_response.json())


def test_read_self_should_return_same_user(read_self_response, user):
    assert UserRead(**read_self_response.json()) == UserRead.from_orm(user)


def test_read_self_should_return_403_for_invalid_jwt(client):
    response = read_self_request(client, 123)
    assert response.status_code == HTTP_403_FORBIDDEN


def test_read_self_should_return_404_if_user_does_not_exist(client, jwt_service):
    jwt_payload = AccessTokenPayload(
        user_id=1, roles=[], exp=AccessTokenPayload.calc_exp(1)
    )
    jwt = jwt_service.generate_token(jwt_payload.dict())
    response = read_self_request(client, jwt)
    assert response.status_code == HTTP_404_NOT_FOUND


def update_self_request(client, jwt, payload=update_payload):
    return client.put(
        "/api/v1/users/me", headers={"Authorization": f"Bearer {jwt}"}, json=payload,
    )


@fixture
def update_self_response(client, user_jwt):
    yield update_self_request(client, user_jwt)


def test_update_self_should_return_status_200_for_valid_jwt(update_self_response):
    assert update_self_response.status_code == HTTP_200_OK


def test_update_self_should_return_json(update_self_response):
    assert update_self_response.headers["Content-Type"] == "application/json"


def test_update_self_should_return_user_schema(update_self_response):
    assert UserRead(**update_self_response.json())


def test_update_self_should_return_same_user(update_self_response, user):
    user.email = update_payload["email"]
    assert UserRead(**update_self_response.json()) == UserRead.from_orm(user)


def test_update_self_should_follow_schema(client, user_jwt):
    update_payload["roles"] = ["ABC", "123"]
    response = update_self_request(client, user_jwt, update_payload)
    assert UserRead(**response.json()).roles == []


def test_update_self_should_return_403_for_invalid_jwt(client):
    response = update_self_request(client, 123)
    assert response.status_code == HTTP_403_FORBIDDEN


def test_update_self_should_return_404_if_user_does_not_exist(client, jwt_service):
    jwt_payload = AccessTokenPayload(
        user_id=1, roles=[], exp=AccessTokenPayload.calc_exp(1)
    )
    jwt = jwt_service.generate_token(jwt_payload.dict())
    response = update_self_request(client, jwt)
    assert response.status_code == HTTP_404_NOT_FOUND


def test_update_self_should_return_409_if_data_conflicts(
    client, jwt_service, user, users_repository
):
    users_repository.create(update_payload)
    jwt_payload = AccessTokenPayload(
        user_id=user.id, roles=user.roles, exp=AccessTokenPayload.calc_exp(1)
    )
    jwt = jwt_service.generate_token(jwt_payload.dict())
    response = update_self_request(client, jwt)
    assert response.status_code == HTTP_409_CONFLICT


def delete_self_request(client, jwt):
    return client.delete(
        "/api/v1/users/me", headers={"Authorization": f"Bearer {jwt}"},
    )


@fixture
def delete_self_response(client, user_jwt, users_repository):
    yield delete_self_request(client, user_jwt)


def test_delete_self_should_return_status_204_for_valid_jwt(delete_self_response):
    assert delete_self_response.status_code == HTTP_204_NO_CONTENT


def test_delete_self_should_return_json(delete_self_response):
    assert delete_self_response.headers["Content-Type"] == "application/json"


def test_delete_self_should_delete_user(delete_self_response, users_repository):
    assert len(users_repository.find_all()) == 0


def test_delete_self_should_return_403_for_invalid_jwt(client):
    response = delete_self_request(client, 123)
    assert response.status_code == HTTP_403_FORBIDDEN


def test_delete_self_should_return_404_if_user_does_not_exist(client, jwt_service):
    jwt_payload = AccessTokenPayload(
        user_id=1, roles=[], exp=AccessTokenPayload.calc_exp(1)
    )
    jwt = jwt_service.generate_token(jwt_payload.dict())
    response = delete_self_request(client, jwt)
    assert response.status_code == HTTP_404_NOT_FOUND

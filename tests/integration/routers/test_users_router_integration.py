from pytest import fixture
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_405_METHOD_NOT_ALLOWED,
    HTTP_409_CONFLICT,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from app.core.models import User, UserRoles
from app.core.schemas import AccessTokenPayload, UserRead

user_dict_1 = {"email": "email@domain.com", "roles": [UserRoles.ADMIN]}
user_dict_2 = {"email": "anotheremail@domain.com"}


@fixture
def user(users_repository):
    return users_repository.create(user_dict_1)


@fixture
def user_jwt(jwt_service, user):
    jwt_payload = AccessTokenPayload(
        user_id=user.id,
        roles=user.roles,
        exp=AccessTokenPayload.calc_exp(1),
        sid="123456",
    )
    return jwt_service.generate_token(jwt_payload.dict())


@fixture
def user_2_jwt(jwt_service, users_repository):
    user = users_repository.create(user_dict_2)
    jwt_payload = AccessTokenPayload(
        user_id=user.id,
        roles=user.roles,
        exp=AccessTokenPayload.calc_exp(1),
        sid="123456",
    )
    return jwt_service.generate_token(jwt_payload.dict())


def list_users_request(client, jwt):
    return client.get("/api/v1/users", headers={"Authorization": f"Bearer {jwt}"})


@fixture
def list_users_response(client, users_repository, user_jwt):
    users_repository.create(user_dict_2)
    yield list_users_request(client, user_jwt)


def test_list_users_should_return_status_200(list_users_response):
    assert list_users_response.status_code == HTTP_200_OK


def test_list_users_should_return_json(list_users_response):
    assert list_users_response.headers["Content-Type"] == "application/json"


def test_list_users_should_return_list(list_users_response):
    assert isinstance(list_users_response.json(), list)


def test_list_users_should_return_list_of_schema(list_users_response):
    assert [UserRead(**user) for user in list_users_response.json()]


def test_list_users_should_return_list_of_users_size(list_users_response):
    assert len(list_users_response.json()) == 2


def test_list_users_should_return_401_for_invalid_jwt(client):
    response = list_users_request(client, 123)
    assert response.status_code == HTTP_401_UNAUTHORIZED


def test_list_users_should_return_403_for_non_admin(client, user_2_jwt):
    response = list_users_request(client, user_2_jwt)
    assert response.status_code == HTTP_403_FORBIDDEN


def read_user_request(client, user_id, jwt):
    return client.get(
        f"/api/v1/users/{user_id}", headers={"Authorization": f"Bearer {jwt}"},
    )


@fixture
def read_user_response(client, user, user_jwt):
    yield read_user_request(client, user.id, user_jwt)


def test_read_user_endpoint_should_accept_get(read_user_response):
    assert read_user_response.status_code != HTTP_405_METHOD_NOT_ALLOWED


def test_read_user_should_return_status_200_if_user_found(read_user_response):
    assert read_user_response.status_code == HTTP_200_OK


def test_read_user_should_return_user_if_found(read_user_response, user):
    response_user = User(**read_user_response.json())
    assert response_user.id == user.id


def test_read_user_should_return_status_404_if_user_not_found(client, user_jwt):
    response = read_user_request(client, 123456, user_jwt)
    assert response.status_code == HTTP_404_NOT_FOUND


def test_read_user_should_return_401_for_invalid_jwt(client):
    response = read_user_request(client, 123, 123)
    assert response.status_code == HTTP_401_UNAUTHORIZED


def test_read_user_should_return_403_for_non_admin(client, user_2_jwt):
    response = read_user_request(client, 123, user_2_jwt)
    assert response.status_code == HTTP_403_FORBIDDEN


def create_user_request(client, payload, jwt):
    return client.post(
        "/api/v1/users", headers={"Authorization": f"Bearer {jwt}"}, json=payload,
    )


@fixture
def create_user_response(client, user_jwt):
    yield create_user_request(client, user_dict_2, user_jwt)


def test_create_user_should_return_status_201(create_user_response):
    assert create_user_response.status_code == HTTP_201_CREATED


def test_create_user_endpoint_should_accept_post(create_user_response):
    assert create_user_response.status_code != HTTP_405_METHOD_NOT_ALLOWED


def test_create_user_should_have_valid_payload(client, user_jwt):
    response = create_user_request(client, {}, user_jwt)
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


def test_create_user_should_return_user_schema(create_user_response):
    assert UserRead(**create_user_response.json())


def test_create_user_should_return_status_409_on_payload_conflict(client, user_jwt):
    response = create_user_request(client, user_dict_1, user_jwt)
    assert response.status_code == HTTP_409_CONFLICT


def test_create_user_should_return_401_for_invalid_jwt(client):
    response = create_user_request(client, {}, 123)
    assert response.status_code == HTTP_401_UNAUTHORIZED


def test_create_user_should_return_403_for_non_admin(client, user_2_jwt):
    response = create_user_request(client, {}, user_2_jwt)
    assert response.status_code == HTTP_403_FORBIDDEN


def delete_user_request(client, user_id, jwt):
    return client.delete(
        f"/api/v1/users/{user_id}", headers={"Authorization": f"Bearer {jwt}"},
    )


@fixture
def delete_user_response(client, user, user_jwt):
    yield delete_user_request(client, user.id, user_jwt)


def test_delete_user_endpoint_should_accept_delete(delete_user_response):
    assert delete_user_response.status_code != HTTP_405_METHOD_NOT_ALLOWED


def test_delete_user_should_return_status_204(delete_user_response):
    assert delete_user_response.status_code == HTTP_204_NO_CONTENT


def test_delete_user_should_remove_user_from_database(
    delete_user_response, users_repository
):
    assert len(users_repository.find_all()) == 0


def test_delete_user_should_return_status_404_if_user_not_found(client, user_jwt):
    response = delete_user_request(client, 123456, user_jwt)
    assert response.status_code == HTTP_404_NOT_FOUND


def test_delete_user_should_return_401_for_invalid_jwt(client):
    response = delete_user_request(client, 123, 123)
    assert response.status_code == HTTP_401_UNAUTHORIZED


def test_delete_user_should_return_403_for_non_admin(client, user_2_jwt):
    response = delete_user_request(client, 123, user_2_jwt)
    assert response.status_code == HTTP_403_FORBIDDEN


def update_user_request(client, user_id, payload, jwt):
    return client.put(
        f"/api/v1/users/{user_id}",
        headers={"Authorization": f"Bearer {jwt}"},
        json=payload,
    )


@fixture
def update_user_response(client, user, user_jwt):
    yield update_user_request(client, user.id, user_dict_2, user_jwt)


def test_update_user_endpoint_should_accept_put(update_user_response):
    assert update_user_response.status_code != HTTP_405_METHOD_NOT_ALLOWED


def test_update_user_should_return_status_200_if_successful(update_user_response):
    assert update_user_response.status_code == HTTP_200_OK


def test_update_user_should_return_user_schema(update_user_response):
    assert UserRead(**update_user_response.json())


def test_update_user_should_return_updated_user(update_user_response):
    assert UserRead(**update_user_response.json()).email == user_dict_2["email"]


def test_update_user_should_not_have_required_fields(client, user, user_jwt):
    response = update_user_request(client, user.id, {}, user_jwt)
    assert response.status_code != HTTP_422_UNPROCESSABLE_ENTITY


def test_update_user_should_return_status_404_if_user_not_found(client, user_jwt):
    response = update_user_request(client, 123456, {}, user_jwt)
    assert response.status_code == HTTP_404_NOT_FOUND


def test_update_user_should_return_status_409_if_payload_has_conflicts(
    client, user, user_jwt, users_repository
):
    users_repository.create(user_dict_2)
    response = update_user_request(client, user.id, user_dict_2, user_jwt)
    assert response.status_code == HTTP_409_CONFLICT


def test_update_user_should_ignore_unknown_fields(client, user, user_jwt):
    update_data = {"key": "value", **user_dict_1}
    response = update_user_request(client, user.id, update_data, user_jwt)
    assert "key" not in response.json()


def test_update_user_should_return_401_for_invalid_jwt(client):
    response = update_user_request(client, 123, {}, 123)
    assert response.status_code == HTTP_401_UNAUTHORIZED


def test_update_user_should_return_403_for_non_admin(client, user_2_jwt):
    response = update_user_request(client, 123, {}, user_2_jwt)
    assert response.status_code == HTTP_403_FORBIDDEN

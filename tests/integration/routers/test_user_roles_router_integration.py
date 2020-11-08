from pytest import fixture
from starlette.status import HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from app.core.models import UserRoles
from app.core.schemas import JWTPayload, UserRead

user_dict = {"email": "email@domain.com", "roles": [UserRoles.ADMIN]}
update_roles = []


@fixture
def user(users_repository):
    return users_repository.create(user_dict)


@fixture
def user_jwt(jwt_service, user):
    return jwt_service.generate_token(JWTPayload(user_id=user.id, roles=user.roles))


def update_user_roles_request(client, user_id, jwt, payload=update_roles):
    return client.put(
        f"/api/v1/users/{user_id}/roles",
        headers={"Authorization": f"Bearer {jwt}"},
        json=payload,
    )


@fixture
def update_user_roles_response(client, user, user_jwt):
    yield update_user_roles_request(client, user.id, user_jwt)


def test_update_user_roles_should_return_status_200_for_valid_jwt(
    update_user_roles_response,
):
    assert update_user_roles_response.status_code == HTTP_200_OK


def test_update_user_roles_should_return_json(update_user_roles_response):
    assert update_user_roles_response.headers["Content-Type"] == "application/json"


def test_update_user_roles_should_return_user_schema(update_user_roles_response):
    assert UserRead(**update_user_roles_response.json())


def test_update_user_roles_should_update_roles(update_user_roles_response, user):
    assert UserRead(**update_user_roles_response.json()).roles == update_roles


def test_update_user_roles_should_return_403_for_invalid_jwt(client):
    response = update_user_roles_request(client, 123, 123, [])
    assert response.status_code == HTTP_403_FORBIDDEN


def test_update_user_should_return_403_for_non_admin(client, jwt_service):
    jwt = jwt_service.generate_token(JWTPayload(user_id=1, roles=[]))
    response = update_user_roles_request(client, 1, jwt, [])
    assert response.status_code == HTTP_403_FORBIDDEN


def test_update_user_roles_should_return_404_if_user_does_not_exist(
    client, jwt_service
):
    jwt = jwt_service.generate_token(JWTPayload(user_id=1, roles=[UserRoles.ADMIN]))
    response = update_user_roles_request(client, 1, jwt, [])
    assert response.status_code == HTTP_404_NOT_FOUND

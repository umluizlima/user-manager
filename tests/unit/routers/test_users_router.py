from datetime import datetime

from pytest import fixture
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_405_METHOD_NOT_ALLOWED,
    HTTP_409_CONFLICT,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from app.core.errors import ResourceAlreadyExistsError, ResourceNotFoundError
from app.core.models import User
from app.core.schemas import UserCreate, UserUpdate

now = datetime.now()
user_dict_1 = {
    "email": "email@domain.com",
}
user_1 = User(id=1, created_at=now, roles=[], **user_dict_1)
user_dict_2 = {
    "email": "anotheremail@domain.com",
}
user_2 = User(id=2, created_at=now, roles=[], **user_dict_2)


@fixture
def list_response(client, mock_repository):
    mock_repository.find_all.return_value = [user_1, user_2]
    yield client.get("/api/v1/users")
    mock_repository.find_all.assert_called_once()


def test_list_should_return_status_200(list_response):
    assert list_response.status_code == HTTP_200_OK


def test_list_should_return_json(list_response):
    assert list_response.headers["Content-Type"] == "application/json"


def test_list_should_return_list(list_response):
    assert isinstance(list_response.json(), list)


def test_listed_user_should_have_id(list_response):
    assert "id" in list_response.json().pop()


def test_listed_user_should_have_email(list_response):
    assert "email" in list_response.json().pop()


def test_listed_user_should_have_created_at(list_response):
    assert "created_at" in list_response.json().pop()


@fixture
def read_response(client, mock_repository):
    mock_repository.find_by_id.return_value = user_1
    yield client.get(f"/api/v1/users/{user_1.id}")
    mock_repository.find_by_id.assert_called_once_with(user_1.id)


def test_read_endpoint_should_accept_get(read_response):
    assert read_response.status_code != HTTP_405_METHOD_NOT_ALLOWED


def test_read_should_return_status_200_if_user_found(read_response):
    assert read_response.status_code == HTTP_200_OK


def test_read_user_should_return_user_if_found(read_response):
    response_user = User(**read_response.json())
    assert response_user.id == user_1.id


def test_read_should_return_status_404_if_user_not_found(client, mock_repository):
    mock_repository.find_by_id.side_effect = ResourceNotFoundError
    response = client.get(f"/api/v1/users/{user_1.id}")
    assert response.status_code == HTTP_404_NOT_FOUND
    mock_repository.find_by_id.assert_called_once_with(user_1.id)


@fixture
def create_response(client, mock_repository):
    mock_repository.create.return_value = user_1
    yield client.post("/api/v1/users", json=user_dict_1)
    mock_repository.create.assert_called_once_with(UserCreate(**user_dict_1).dict())


def test_create_user_endpoint_should_accept_post(create_response):
    assert create_response.status_code != HTTP_405_METHOD_NOT_ALLOWED


def test_create_user_should_have_amount(client):
    response = client.post("/api/v1/users", json={})
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


def test_create_user_should_return_user(create_response):
    assert create_response.json()["id"] == user_1.id


def test_created_user_should_return_status_201(create_response):
    assert create_response.status_code == HTTP_201_CREATED


def test_create_user_should_return_status_409_on_payload_conflict(
    client, mock_repository
):
    mock_repository.create.side_effect = ResourceAlreadyExistsError
    response = client.post("/api/v1/users", json=user_dict_1)
    assert response.status_code == HTTP_409_CONFLICT
    mock_repository.create.assert_called_once_with(user_dict_1)


@fixture
def delete_response(client, mock_repository):
    mock_repository.delete_by_id.reset_mock()
    yield client.delete(f"/api/v1/users/{user_1.id}")
    mock_repository.delete_by_id.assert_called_once_with(user_1.id)


def test_delete_user_endpoint_should_accept_delete(delete_response):
    assert delete_response.status_code != HTTP_405_METHOD_NOT_ALLOWED


def test_delete_user_should_return_status_204(delete_response):
    assert delete_response.status_code == HTTP_204_NO_CONTENT


def test_delete_user_should_return_status_404_if_user_not_found(
    client, mock_repository
):
    mock_repository.delete_by_id.side_effect = ResourceNotFoundError
    response = client.delete(f"/api/v1/users/{user_1.id}")
    assert response.status_code == HTTP_404_NOT_FOUND
    mock_repository.delete_by_id.assert_called_once_with(user_1.id)


@fixture
def update_response(client, mock_repository):
    mock_repository.reset_mock()
    mock_repository.update_by_id.return_value = user_1
    yield client.put(f"/api/v1/users/{user_1.id}", json=user_dict_1)
    mock_repository.update_by_id.assert_called_once_with(
        user_1.id, UserUpdate(**user_dict_1).dict()
    )


def test_update_user_endpoint_should_accept_put(update_response):
    assert update_response.status_code != HTTP_405_METHOD_NOT_ALLOWED


def test_update_user_should_return_updated_user(update_response):
    assert update_response.json()["email"] == user_dict_1["email"]


def test_update_user_should_return_status_200_if_successful(update_response):
    assert update_response.status_code == HTTP_200_OK


def test_update_user_should_not_have_required_fields(client):
    response = client.put(f"/api/v1/users/{user_1.id}", json={})
    assert response.status_code != HTTP_422_UNPROCESSABLE_ENTITY


def test_update_user_should_return_status_404_if_user_not_found(
    client, mock_repository
):
    mock_repository.update_by_id.side_effect = ResourceNotFoundError
    response = client.put(f"/api/v1/users/{user_1.id}", json=user_dict_1)
    assert response.status_code == HTTP_404_NOT_FOUND
    mock_repository.update_by_id.assert_called_once_with(
        user_1.id, UserUpdate(**user_dict_1).dict()
    )


def test_update_user_should_return_status_409_if_payload_has_conflicts(
    client, mock_repository
):
    mock_repository.update_by_id.side_effect = ResourceAlreadyExistsError
    response = client.put(f"/api/v1/users/{user_1.id}", json=user_dict_1)
    assert response.status_code == HTTP_409_CONFLICT
    mock_repository.update_by_id.assert_called_once_with(
        user_1.id, UserUpdate(**user_dict_1).dict()
    )


def test_update_user_should_ignore_unknown_fields(client, mock_repository):
    update_data = {"key": "value", **user_dict_1}
    mock_repository.update_by_id.return_value = user_1
    client.put(f"/api/v1/users/{user_1.id}", json=update_data)
    mock_repository.update_by_id.assert_called_once_with(
        user_1.id, UserUpdate(**user_dict_1).dict()
    )

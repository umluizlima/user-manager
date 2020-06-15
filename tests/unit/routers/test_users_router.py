from datetime import datetime
from decimal import Decimal
from unittest.mock import MagicMock

from pytest import fixture
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_405_METHOD_NOT_ALLOWED,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from app.api import api
from app.core.database import get_db
from app.core.models import User
from app.core.repositories import UsersRepository
from app.core.schemas import UserCreate, UserRead, UserUpdate


def mock_get_db():
    return MagicMock()


api.dependency_overrides[get_db] = mock_get_db

now = datetime.now()
user_dict_1 = {
    "email": "email@domain.com",
}
user_1 = User(id=1, created_at=now, **user_dict_1)
user_dict_2 = {
    "email": "anotheremail@domain.com",
}
user_2 = User(id=2, created_at=now, **user_dict_2)


@fixture(scope="function")
def list_response(client):
    UsersRepository.find_all = MagicMock(return_value=[user_1, user_2])
    yield client.get("/api/v1/users")
    UsersRepository.find_all.assert_called_once()


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


@fixture(scope="function")
def read_response(client):
    UsersRepository.find_by_id = MagicMock(return_value=user_1)
    yield client.get(f"/api/v1/users/{user_1.id}")
    UsersRepository.find_by_id.assert_called_once_with(user_1.id)


def test_read_endpoint_should_accept_get(read_response):
    assert read_response.status_code != HTTP_405_METHOD_NOT_ALLOWED


def test_read_should_return_status_200_if_user_found(read_response):
    assert read_response.status_code == HTTP_200_OK


def test_read_user_should_return_user_if_found(read_response):
    response_user = User(**read_response.json())
    assert response_user.id == user_1.id


def test_read_should_return_status_404_if_user_not_found(client):
    UsersRepository.find_by_id = MagicMock(side_effect=Exception)
    response = client.get(f"/api/v1/users/{user_1.id}")
    assert response.status_code == HTTP_404_NOT_FOUND
    UsersRepository.find_by_id.assert_called_once_with(user_1.id)


@fixture(scope="function")
def create_response(client):
    UsersRepository.create = MagicMock(return_value=user_1)
    yield client.post("/api/v1/users", json=user_dict_1)
    UsersRepository.create.assert_called_once_with(UserCreate(**user_dict_1).dict())


def test_create_user_endpoint_should_accept_post(create_response):
    assert create_response.status_code != HTTP_405_METHOD_NOT_ALLOWED


def test_create_user_should_have_amount(client):
    response = client.post("/api/v1/users", json={})
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


def test_create_user_should_return_user(create_response):
    assert create_response.json()["id"] == user_1.id


def test_created_user_should_return_status_201(create_response):
    assert create_response.status_code == HTTP_201_CREATED


@fixture(scope="function")
def delete_response(client):
    UsersRepository.delete_by_id = MagicMock()
    yield client.delete(f"/api/v1/users/{user_1.id}")
    UsersRepository.delete_by_id.assert_called_once_with(user_1.id)


def test_delete_user_endpoint_should_accept_delete(delete_response):
    print(delete_response.status_code)
    assert delete_response.status_code != HTTP_405_METHOD_NOT_ALLOWED


def test_delete_user_should_return_status_204(delete_response):
    assert delete_response.status_code == HTTP_204_NO_CONTENT


def test_delete_user_should_return_status_404_if_user_not_found(client):
    UsersRepository.delete_by_id = MagicMock(side_effect=Exception)
    response = client.delete(f"/api/v1/users/{user_1.id}")
    assert response.status_code == HTTP_404_NOT_FOUND
    UsersRepository.delete_by_id.assert_called_once_with(user_1.id)


@fixture(scope="function")
def update_response(client):
    UsersRepository.update_by_id = MagicMock(return_value=user_1)
    yield client.put(f"/api/v1/users/{user_1.id}", json=user_dict_1)
    UsersRepository.update_by_id.assert_called_once_with(
        user_1.id, UserUpdate(**user_dict_1).dict()
    )


def test_update_user_endpoint_should_accept_put(update_response):
    assert update_response.status_code != HTTP_405_METHOD_NOT_ALLOWED


def test_update_user_should_return_status_404_if_user_not_found(client):
    UsersRepository.update_by_id = MagicMock(side_effect=Exception)
    response = client.put(f"/api/v1/users/{user_1.id}", json=user_dict_1)
    assert response.status_code == HTTP_404_NOT_FOUND
    UsersRepository.update_by_id.assert_called_once_with(
        user_1.id, UserUpdate(**user_dict_1).dict()
    )


def test_update_user_should_not_have_required_fields(client):
    response = client.put(f"/api/v1/users/{user_1.id}", json={})
    assert response.status_code != HTTP_422_UNPROCESSABLE_ENTITY


def test_update_user_should_return_updated_user(update_response):
    assert update_response.json()["email"] == user_dict_1["email"]


def test_update_user_should_ignore_unknown_fields(client):
    update_data = {"key": "value", **user_dict_1}
    UsersRepository.update_by_id = MagicMock(return_value=user_1)
    client.put(f"/api/v1/users/{user_1.id}", json=update_data)
    UsersRepository.update_by_id.assert_called_once_with(
        user_1.id, UserUpdate(**user_dict_1).dict()
    )


def test_update_user_should_return_status_200_if_successful(update_response):
    assert update_response.status_code == HTTP_200_OK

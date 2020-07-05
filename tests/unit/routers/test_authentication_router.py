from datetime import datetime

from pytest import fixture
from starlette.status import (
    HTTP_200_OK,
    HTTP_202_ACCEPTED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from app.core.errors import ResourceNotFoundError
from app.core.models import User
from app.core.schemas import TokenCreate, Token

now = datetime.now()
code = "123456"
jwt = "headers.payload.signature"
body_1 = TokenCreate(email="email@domain.com", create_user=False)
user_1 = User(id=1, created_at=now, email="email@domain.com")
body_2 = TokenCreate(email="anotheremail@domain.com", create_user=True)
user_2 = User(id=2, created_at=now, email="anotheremail@domain.com")


def test_generate_code_should_return_status_202(client, mock_dependency):
    mock_dependency.find_by_email.return_value = user_1
    mock_dependency.generate_code.return_value = code
    response = client.post("/api/v1/authentication", json=body_1.dict())
    assert response.status_code == HTTP_202_ACCEPTED


def test_generate_code_should_return_status_404_if_user_is_not_found(
    client, mock_dependency
):
    mock_dependency.find_by_email.side_effect = ResourceNotFoundError
    response = client.post("/api/v1/authentication", json=body_1.dict())
    assert response.status_code == HTTP_404_NOT_FOUND


def test_generate_code_should_create_user_if_does_not_exist_and_parameter_is_passed(
    client, mock_dependency
):
    mock_dependency.find_by_email.side_effect = ResourceNotFoundError
    mock_dependency.create.return_value = user_2
    mock_dependency.generate_code.return_value = code
    response = client.post("/api/v1/authentication", json=body_2.dict())
    assert response.status_code == HTTP_202_ACCEPTED


def test_generate_code_should_send_code_if_user_exists(client, mock_dependency):
    mock_dependency.find_by_email.return_value = user_1
    mock_dependency.find_by_email.side_effect = None
    mock_dependency.generate_code.return_value = code
    client.post("/api/v1/authentication", json=body_1.dict())
    mock_dependency.send_code.assert_called_once_with(code, user_1.email)


def test_retrieve_token_should_return_status_200(client, mock_dependency):
    mock_dependency.find_by_email.return_value = user_1
    mock_dependency.find_by_email.side_effect = None
    mock_dependency.verify_code.return_value = True
    mock_dependency.generate_token.return_value = jwt
    response = client.get(f"/api/v1/authentication?email={user_1.email}&code={code}")
    assert response.status_code == HTTP_200_OK


def test_retrieve_token_should_return_token(client, mock_dependency):
    mock_dependency.find_by_email.return_value = user_1
    mock_dependency.find_by_email.side_effect = None
    mock_dependency.verify_code.return_value = True
    mock_dependency.generate_token.return_value = jwt
    response = client.get(f"/api/v1/authentication?email={user_1.email}&code={code}")
    assert Token(**response.json()).access_token == jwt


def test_retrieve_token_should_return_status_404_if_user_not_found(
    client, mock_dependency
):
    mock_dependency.find_by_email.side_effect = ResourceNotFoundError
    response = client.get(f"/api/v1/authentication?email={user_1.email}&code={code}")
    assert response.status_code == HTTP_404_NOT_FOUND


def test_retrieve_token_should_return_status_400_if_code_is_invalid(
    client, mock_dependency
):
    mock_dependency.find_by_email.return_value = user_1
    mock_dependency.find_by_email.side_effect = None
    mock_dependency.verify_code.return_value = False
    response = client.get(f"/api/v1/authentication?email={user_1.email}&code={code}")
    assert response.status_code == HTTP_400_BAD_REQUEST

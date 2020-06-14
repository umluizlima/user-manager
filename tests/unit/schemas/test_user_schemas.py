from datetime import datetime

from pydantic.error_wrappers import ValidationError
from pytest import raises

from app.core.schemas import UserCreate, UserRead, UserUpdate

new_user = {
    "email": "email@domain.com",
}


def test_user_create_must_have_email():
    new_user_without_email = {**new_user}
    del new_user_without_email["email"]
    with raises(ValidationError):
        UserCreate(**new_user_without_email)


def test_read_must_have_id():
    with raises(ValidationError):
        UserRead(**new_user, created_at=datetime.now())


def test_read_must_have_created_at():
    with raises(ValidationError):
        UserRead(**new_user, id=123)


def test_user_email_must_match_pattern():
    invalid_email = "abc"
    with raises(ValidationError):
        UserUpdate(email=invalid_email)

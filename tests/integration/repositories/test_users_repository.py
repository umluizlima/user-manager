from datetime import datetime
from decimal import Decimal

from pytest import fixture, raises
from sqlalchemy.orm.exc import NoResultFound

from app.core.models import User
from app.core.repositories import UsersRepository


@fixture(scope="function")
def repository(db):
    return UsersRepository(db)


new_user = {
    "email": "email@domain.com",
}
new_user_2 = {
    "email": "anotheremail@domain.com",
}


def test_create_should_return_user_instance(repository):
    user = repository.create(new_user)
    assert isinstance(user, User)


def test_create_user_should_have_base_attributes(repository):
    user = repository.create(new_user)
    assert user.id
    assert isinstance(user.created_at, datetime)
    assert isinstance(user.updated_at, datetime)


def test_create_user_should_have_given_attributes(repository):
    user = repository.create(new_user)
    assert user.email == new_user["email"]


def test_create_users_should_be_persisted(repository):
    repository.create(new_user)
    repository.create(new_user_2)
    assert len(repository.find_all()) == 2


def test_find_all_should_return_list(repository):
    assert isinstance(repository.find_all(), list)


def test_find_all_should_return_existing_users(repository):
    user = repository.create(new_user)
    result = repository.find_all()
    assert result[0] == user


def test_find_by_id_should_return_user(repository):
    user = repository.create(new_user)
    result = repository.find_by_id(user.id)
    assert result.id == user.id


def test_find_by_id_should_raise_exception_if_not_found(repository):
    with raises(NoResultFound):
        repository.find_by_id(123)


def test_update_by_id_should_update_user(repository):
    user = repository.create(new_user)
    updated_user = repository.update_by_id(user.id, {"email": "newemail@domain.com"})
    assert updated_user.email == "newemail@domain.com"


def test_update_by_id_should_raise_exception_if_not_found(repository):
    with raises(NoResultFound):
        repository.update_by_id(123, {})


def test_delete_by_id_should_remove_user(repository):
    user = repository.create(new_user)
    repository.delete_by_id(user.id)
    assert user not in repository.find_all()


def test_delete_by_id_should_raise_exception_if_not_found(repository):
    with raises(NoResultFound):
        repository.delete_by_id(123)

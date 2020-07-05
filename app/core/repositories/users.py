from pydantic import EmailStr
from sqlalchemy.orm.exc import NoResultFound

from ..errors import ResourceNotFoundError
from ..models import User
from .base import BaseRepository


class UsersRepository(BaseRepository):
    __model__ = User

    def find_by_email(self, email: EmailStr) -> User:
        try:
            return self._filter_by_email(email).one()
        except NoResultFound:
            raise ResourceNotFoundError

    def _filter_by_email(self, email: EmailStr):
        return self.db.query(self.__model__).filter(self.__model__.email == email)

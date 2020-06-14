from ..models import User
from .base import BaseRepository


class UsersRepository(BaseRepository):
    __model__ = User

from abc import ABC, abstractmethod
from typing import Dict, List

from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError, InvalidRequestError

from ..errors import ResourceAlreadyExistsError, ResourceNotFoundError
from ..models import BaseModel


class BaseRepository(ABC):
    @property
    @abstractmethod
    def __model__(self) -> BaseModel:
        ...

    def __init__(self, db: Session):
        self.db = db

    def save(self, obj: BaseModel) -> BaseModel:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def find_all(self) -> List[BaseModel]:
        return self.db.query(self.__model__).all()

    def find_by_id(self, id: int) -> BaseModel:
        try:
            return self._filter_by_id(id).one()
        except NoResultFound:
            raise ResourceNotFoundError

    def delete_by_id(self, id: int):
        if not self._filter_by_id(id).delete():
            raise ResourceNotFoundError

    def create(self, data: Dict) -> BaseModel:
        try:
            return self.save(self.__model__(**data))
        except IntegrityError:
            raise ResourceAlreadyExistsError

    def update_by_id(self, id: int, data: Dict):
        try:
            if not self._filter_by_id(id).update(data):
                raise ResourceNotFoundError
        except IntegrityError:
            raise ResourceAlreadyExistsError
        return self.find_by_id(id)

    def _filter_by_id(self, id: id):
        return self.db.query(self.__model__).filter(self.__model__.id == id)

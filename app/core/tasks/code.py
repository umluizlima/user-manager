from pydantic import EmailStr

from app.core.schemas import Transactional, TransactionalSchema

from .base import Task
from .producer import TasksProducer


class SendCodeProducer(TasksProducer):
    def send_code(self, code: str, email: EmailStr):
        message = TransactionalSchema(
            to=email, type=Transactional.ACCESS_CODE, data={"code": code},
        )
        self._producer.send_task(
            Task.SEND_TRANSACTIONAL, args=[message.dict(by_alias=True)]
        )

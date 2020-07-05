from pydantic import EmailStr

from app.core.schemas import EmailSchema

from .base import Task
from .producer import TasksProducer


class SendCodeProducer(TasksProducer):
    def send_code(self, code: str, email: EmailStr):
        message = EmailSchema(
            to=email,
            subject=self._settings.ACCESS_CODE_MESSAGE_SUBJECT.format(code),
            content=self._settings.ACCESS_CODE_MESSAGE_CONTENT.format(code),
        )
        self._producer.send_task(Task.SEND_EMAIL, args=[message.dict()])

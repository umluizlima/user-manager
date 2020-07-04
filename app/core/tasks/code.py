from pydantic import EmailStr

from app.core.schemas import EmailSchema

from .base import Task
from .producer import TasksProducer


class SendCodeProducer(TasksProducer):
    MESSAGE_SUBJECT = "Access code: {}"
    MESSAGE_CONTENT = "{} is your code to access user-manager"

    def send_code(self, code: str, email: EmailStr):
        message = EmailSchema(
            to=email,
            subject=SendCodeProducer.MESSAGE_SUBJECT.format(code),
            content=SendCodeProducer.MESSAGE_CONTENT.format(code),
        )
        self._producer.send_task(Task.SEND_EMAIL, args=[message.dict()])

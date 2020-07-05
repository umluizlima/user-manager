from fastapi import Depends

from app.core.tasks import SendCodeProducer
from app.settings import get_settings, Settings


def send_code_producer(settings: Settings = Depends(get_settings)):
    return SendCodeProducer(settings)

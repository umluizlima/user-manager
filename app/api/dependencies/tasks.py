from fastapi import Depends

from app.core.tasks import SendCodeProducer
from app.settings import Settings, get_settings


def send_code_producer(settings: Settings = Depends(get_settings)):
    return SendCodeProducer(settings)

import logging

from fastapi import FastAPI

from app.settings import Environment, Settings


def configure(app: FastAPI, settings: Settings):
    level = logging.DEBUG if settings.ENV == Environment.DEVELOPMENT else logging.INFO
    logging.basicConfig(format="%(levelname)s: %(asctime)s - %(message)s", level=level)

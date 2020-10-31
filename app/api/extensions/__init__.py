from fastapi import FastAPI

from app.settings import Settings

from . import https, sentry


def configure(app: FastAPI, settings: Settings):
    for extension in [https, sentry]:
        extension.configure(app, settings)

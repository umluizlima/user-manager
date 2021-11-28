from fastapi import FastAPI

from app.settings import Settings

from . import https, logging, sentry


def configure(app: FastAPI, settings: Settings):
    for extension in [https, logging, sentry]:
        extension.configure(app, settings)

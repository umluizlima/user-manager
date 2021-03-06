import sentry_sdk
from fastapi import FastAPI
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from app.settings import Environment, Settings


def configure(app: FastAPI, settings: Settings):
    if settings.SENTRY_DSN and settings.ENV != Environment.DEVELOPMENT:
        sentry_sdk.init(settings.SENTRY_DSN)
        app.add_middleware(SentryAsgiMiddleware)

from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

from app.settings import Environment, Settings


def configure(app: FastAPI, settings: Settings):
    if settings.ENV != Environment.DEVELOPMENT:
        app.add_middleware(HTTPSRedirectMiddleware)

from fastapi import FastAPI

from app.settings import Settings

from . import authentication, user_current, users


def configure(app: FastAPI, settings: Settings):
    for router in [authentication, user_current, users]:
        router.configure(app, settings)

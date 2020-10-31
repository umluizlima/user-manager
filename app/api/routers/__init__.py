from fastapi import FastAPI

from app.settings import Settings

from . import authentication, users


def configure(app: FastAPI, settings: Settings):
    for router in [authentication, users]:
        router.configure(app, settings)

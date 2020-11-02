from fastapi import FastAPI

from app.settings import Settings

from . import authentication, user_current, user_roles, users


def configure(app: FastAPI, settings: Settings):
    for router in [authentication, user_current, users, user_roles]:
        router.configure(app, settings)

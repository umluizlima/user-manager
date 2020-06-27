from fastapi import FastAPI

from ..settings import Settings
from . import extensions, routers


def create_api(settings: Settings):
    api = FastAPI(title="user-manager")

    extensions.configure(api, settings)
    routers.configure(api, settings)

    return api

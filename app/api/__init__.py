from fastapi import FastAPI

from ..settings import settings
from . import extensions, routers

api = FastAPI(title="user-manager")

extensions.configure(api, settings)
routers.configure(api, settings)

from fastapi import Depends

from .users import router as users_router


def configure(app, settings):
    app.include_router(
        users_router, tags=["users"], prefix="/api/v1",
    )

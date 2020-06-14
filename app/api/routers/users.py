from typing import List

from fastapi import APIRouter
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
)

router = APIRouter()


@router.post("/users", status_code=HTTP_201_CREATED)
def create():
    return "Create user"


@router.get("/users", response_model=List)
def list():
    return []


@router.get("/users/{user_id}")
def read(user_id: int):
    return f"Read user {user_id}"


@router.put("/users/{user_id}")
def update(user_id: int):
    return f"Update user {user_id}"


@router.delete("/users/{users_id}", status_code=HTTP_204_NO_CONTENT)
def delete(user_id: int):
    return f"Delete user {user_id}"

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
)

from app.core.database import get_db
from app.core.repositories import UsersRepository
from app.core.schemas import UserCreate, UserRead, UserUpdate

router = APIRouter()


@router.post("/users", response_model=UserRead, status_code=HTTP_201_CREATED)
def create(user: UserCreate, db: Session = Depends(get_db)):
    return UsersRepository(db).create(user.dict())


@router.get("/users", response_model=List[UserRead])
def list(db: Session = Depends(get_db)):
    return UsersRepository(db).find_all()


@router.get("/users/{user_id}", response_model=UserRead)
def read(user_id: int, db: Session = Depends(get_db)):
    try:
        return UsersRepository(db).find_by_id(user_id)
    except Exception:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")


@router.put("/users/{user_id}", response_model=UserRead)
def update(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    try:
        return UsersRepository(db).update_by_id(user_id, user.dict(exclude_unset=True))
    except Exception:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")


@router.delete("/users/{user_id}", status_code=HTTP_204_NO_CONTENT)
def delete(user_id: int, db: Session = Depends(get_db)):
    try:
        return UsersRepository(db).delete_by_id(user_id)
    except Exception:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")

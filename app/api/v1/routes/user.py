from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.schemas.user import User, UserCreate, UserUpdate
from app.services.user import user_service
from app.db.session import get_db

router = APIRouter()


@router.get("/users/", response_model=List[User])
def list_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Retrieve users.
    """
    users = user_service.get_users(db, skip=skip, limit=limit)
    return users


@router.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
):
    """
    Create new user.
    """
    user = user_service.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = user_service.create_user(db, user_in=user_in)
    return user


@router.get("/users/{user_id}", response_model=User)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    """
    Get a specific user by id.
    """
    user = user_service.get_user(db, user_id=user_id)
    return user


@router.put("/users/{user_id}", response_model=User)
def update_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    user_in: UserUpdate,
):
    """
    Update a user.
    """
    user = user_service.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist in the system",
        )
    user = user_service.update_user(db, user_id=user_id, user_in=user_in)
    return user


@router.delete("/users/{user_id}", response_model=User)
def delete_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
):
    """
    Delete a user.
    """
    user = user_service.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist in the system",
        )
    user = user_service.delete_user(db, user_id=user_id)
    return user 
# app/api/v1/endpoints/users.py
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_superuser, get_current_active_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import User as UserSchema, UserCreate, UserUpdate
from app.services.user import create_user, get_user, get_users, update_user, delete_user

router = APIRouter()


@router.get("/users/", response_model=List[UserSchema])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    """
    users = await get_users(db, skip=skip, limit=limit)
    return users


@router.post("/users/", response_model=UserSchema)
async def create_new_user(
    *,
    db: AsyncSession = Depends(get_db),
    user_in: UserCreate,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    Create new user.
    """
    user = await get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = await create_user(db, user_create=user_in)
    return user


@router.get("/users/me", response_model=UserSchema)
async def read_user_me(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.get("/users/{user_id}", response_model=UserSchema)
async def read_user_by_id(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = await get_user(db, id=user_id)
    if user == current_user:
        return user
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return user


@router.put("/users/{user_id}", response_model=UserSchema)
async def update_user_by_id(
    *,
    db: AsyncSession = Depends(get_db),
    user_id: int,
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    Update a user.
    """
    user = await get_user(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist in the system",
        )
    user = await update_user(db, db_obj=user, obj_in=user_in)
    return user


@router.delete("/users/{user_id}", response_model=UserSchema)
async def delete_user_by_id(
    *,
    db: AsyncSession = Depends(get_db),
    user_id: int,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    Delete a user.
    """
    user = await get_user(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist in the system",
        )
    user = await delete_user(db, id=user_id)
    return user

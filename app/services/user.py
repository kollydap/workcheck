# app/services/user.py
from typing import Any, Dict, Optional, Union, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


async def get_user(db: AsyncSession, id: int) -> Optional[User]:
    result = await db.execute(select(User).filter(User.id == id))
    return result.scalars().first()


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()


async def get_users(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> List[User]:
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()


async def create_user(db: AsyncSession, user_create: UserCreate) -> User:
    db_user = User(
        email=user_create.email,
        hashed_password=get_password_hash(user_create.password),
        full_name=user_create.full_name,
        is_superuser=user_create.is_superuser,
        is_active=user_create.is_active,
        company_id=user_create.company_id
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def update_user(
    db: AsyncSession, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
) -> User:
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.dict(exclude_unset=True)
    
    if update_data.get("password"):
        hashed_password = get_password_hash(update_data["password"])
        del update_data["password"]
        update_data["hashed_password"] = hashed_password
    
    for field in update_data:
        if hasattr(db_obj, field):
            setattr(db_obj, field, update_data[field])
    
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def delete_user(db: AsyncSession, id: int) -> Optional[User]:
    user = await get_user(db, id=id)
    if user:
        await db.delete(user)
        await db.commit()
    return user


async def authenticate_user(db: AsyncSession, email: str, password: str) -> Optional[User]:
    user = await get_user_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


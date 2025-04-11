# app/services/company.py
from typing import Any, Dict, Optional, Union, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyUpdate


async def get_company(db: AsyncSession, id: int) -> Optional[Company]:
    result = await db.execute(select(Company).filter(Company.id == id))
    return result.scalars().first()


async def get_companies(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> List[Company]:
    result = await db.execute(select(Company).offset(skip).limit(limit))
    return result.scalars().all()


async def create_company(db: AsyncSession, obj_in: CompanyCreate) -> Company:
    db_obj = Company(
        name=obj_in.name,
        address=obj_in.address,
        description=obj_in.description,
        is_active=obj_in.is_active
    )
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def update_company(
    db: AsyncSession, db_obj: Company, obj_in: Union[CompanyUpdate, Dict[str, Any]]
) -> Company:
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.dict(exclude_unset=True)
    
    for field in update_data:
        if hasattr(db_obj, field):
            setattr(db_obj, field, update_data[field])
    
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def delete_company(db: AsyncSession, id: int) -> Optional[Company]:
    company = await get_company(db, id=id)
    if company:
        await db.delete(company)
        await db.commit()
    return company

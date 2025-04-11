# app/api/v1/endpoints/companies.py
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_superuser, get_current_active_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.company import (
    Company,
    CompanyCreate,
    CompanyUpdate,
    CompanyWithEmployees,
)
from app.services.company import (
    create_company,
    get_company,
    get_companies,
    update_company,
    delete_company,
)

router = APIRouter()


@router.get("/companies/", response_model=List[Company])
async def read_companies(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve companies.
    """
    if current_user.is_superuser:
        companies = await get_companies(db, skip=skip, limit=limit)
    else:
        # Regular users can only see their own company
        companies = [current_user.company] if current_user.company else []
    return companies


@router.post("/companies/", response_model=Company)
async def create_new_company(
    *,
    db: AsyncSession = Depends(get_db),
    company_in: CompanyCreate,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    Create new company.
    """
    company = await create_company(db=db, obj_in=company_in)
    return company


@router.get("/companies/{company_id}", response_model=CompanyWithEmployees)
async def read_company_by_id(
    company_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get a specific company by id.
    """
    company = await get_company(db, id=company_id)
    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found",
        )
    if not current_user.is_superuser and (
        not current_user.company or current_user.company.id != company_id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return company


@router.put("/companies/{company_id}", response_model=Company)
async def update_company_by_id(
    *,
    db: AsyncSession = Depends(get_db),
    company_id: int,
    company_in: CompanyUpdate,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    Update a company.
    """
    company = await get_company(db, id=company_id)
    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found",
        )
    company = await update_company(db=db, db_obj=company, obj_in=company_in)
    return company


@router.delete("/companies/{company_id}", response_model=Company)
async def delete_company_by_id(
    *,
    db: AsyncSession = Depends(get_db),
    company_id: int,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    Delete a company.
    """
    company = await get_company(db, id=company_id)
    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found",
        )
    company = await delete_company(db=db, id=company_id)
    return company

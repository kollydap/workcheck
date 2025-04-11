# app/schemas/company.py
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

from app.schemas.user import User


# Shared properties
class CompanyBase(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = True


# Properties to receive via API on creation
class CompanyCreate(CompanyBase):
    name: str
    address: str


# Properties to receive via API on update
class CompanyUpdate(CompanyBase):
    pass


# Additional properties stored in DB
class CompanyInDBBase(CompanyBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Company(CompanyInDBBase):
    pass


# Company with employees
class CompanyWithEmployees(Company):
    employees: List[User] = []

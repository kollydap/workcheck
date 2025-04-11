# app/schemas/attendance.py
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


# Shared properties
class AttendanceBase(BaseModel):
    user_id: int
    check_in: Optional[datetime] = None
    check_out: Optional[datetime] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    check_in_method: Optional[str] = None  # "QR", "NFC", "MANUAL"
    check_out_method: Optional[str] = None  # "QR", "NFC", "MANUAL"
    notes: Optional[str] = None


# Properties to receive via API on check-in
class AttendanceCheckIn(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    check_in_method: str = Field(..., regex="^(QR|NFC|MANUAL)$")
    notes: Optional[str] = None


# Properties to receive via API on check-out
class AttendanceCheckOut(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    check_out_method: str = Field(..., regex="^(QR|NFC|MANUAL)$")
    notes: Optional[str] = None


# Properties to receive via API on creation (admin)
class AttendanceCreate(AttendanceBase):
    user_id: int
    check_in: datetime


# Properties to receive via API on update
class AttendanceUpdate(BaseModel):
    check_out: Optional[datetime] = None
    notes: Optional[str] = None


# Additional properties stored in DB
class AttendanceInDBBase(AttendanceBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Attendance(AttendanceInDBBase):
    pass
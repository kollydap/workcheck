# app/api/v1/endpoints/attendance.py
from typing import Any, List
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.attendance import (
    Attendance as AttendanceSchema,
    AttendanceCheckIn,
    AttendanceCheckOut,
    AttendanceCreate,
    AttendanceUpdate,
)
from app.services.attendance import (
    check_in,
    check_out,
    create_attendance,
    get_attendance,
    get_attendance_by_date_range,
    get_attendance_by_user,
    get_user_current_status,
    update_attendance,
)

router = APIRouter()


@router.post("/attendance/check-in", response_model=AttendanceSchema)
async def user_check_in(
    *,
    db: AsyncSession = Depends(get_db),
    check_in_data: AttendanceCheckIn,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    User check-in.
    """
    status = await get_user_current_status(db, user_id=current_user.id)
    if status and not status.check_out:
        raise HTTPException(
            status_code=400,
            detail="You are already checked in. Please check out first.",
        )

    attendance = await check_in(
        db=db,
        user_id=current_user.id,
        latitude=check_in_data.latitude,
        longitude=check_in_data.longitude,
        check_in_method=check_in_data.check_in_method,
        notes=check_in_data.notes,
    )
    return attendance


@router.post("/attendance/check-out", response_model=AttendanceSchema)
async def user_check_out(
    *,
    db: AsyncSession = Depends(get_db),
    check_out_data: AttendanceCheckOut,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    User check-out.
    """
    status = await get_user_current_status(db, user_id=current_user.id)
    if not status or status.check_out:
        raise HTTPException(
            status_code=400,
            detail="You are not checked in. Please check in first.",
        )

    attendance = await check_out(
        db=db,
        attendance_id=status.id,
        latitude=check_out_data.latitude,
        longitude=check_out_data.longitude,
        check_out_method=check_out_data.check_out_method,
        notes=check_out_data.notes,
    )
    return attendance


@router.get("/attendance/status", response_model=AttendanceSchema)
async def get_current_status(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get current user's attendance status.
    """
    status = await get_user_current_status(db, user_id=current_user.id)
    if not status:
        raise HTTPException(
            status_code=404,
            detail="No active attendance record found.",
        )
    return status


@router.get("/attendance/", response_model=List[AttendanceSchema])
async def read_attendance(
    *,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
    start_date: datetime = Query(None),
    end_date: datetime = Query(None),
) -> Any:
    """
    Retrieve attendance records.
    """
    if current_user.is_superuser:
        if start_date and end_date:
            attendance = await get_attendance_by_date_range(
                db, start_date=start_date, end_date=end_date, skip=skip, limit=limit
            )
        else:
            attendance = await get_attendance(db, skip=skip, limit=limit)
    else:
        if start_date and end_date:
            attendance = await get_attendance_by_date_range(
                db,
                start_date=start_date,
                end_date=end_date,
                user_id=current_user.id,
                skip=skip,
                limit=limit,
            )
        else:
            attendance = await get_attendance_by_user(
                db, user_id=current_user.id, skip=skip, limit=limit
            )
    return attendance


@router.post("/attendance/", response_model=AttendanceSchema)
async def create_attendance_record(
    *,
    db: AsyncSession = Depends(get_db),
    attendance_in: AttendanceCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create new attendance record (admin only).
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    attendance = await create_attendance(db=db, obj_in=attendance_in)
    return attendance


@router.get("/attendance/{attendance_id}", response_model=AttendanceSchema)
async def read_attendance_by_id(
    *,
    db: AsyncSession = Depends(get_db),
    attendance_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get a specific attendance record by id.
    """
    attendance = await get_attendance(db, id=attendance_id)
    if not attendance:
        raise HTTPException(
            status_code=404,
            detail="Attendance record not found",
        )
    if not current_user.is_superuser and attendance.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return attendance


@router.put("/attendance/{attendance_id}", response_model=AttendanceSchema)
async def update_attendance_record(
    *,
    db: AsyncSession = Depends(get_db),
    attendance_id: int,
    attendance_in: AttendanceUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update an attendance record (admin only).
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    attendance = await get_attendance(db, id=attendance_id)
    if not attendance:
        raise HTTPException(
            status_code=404,
            detail="Attendance record not found",
        )
    attendance = await update_attendance(db=db, db_obj=attendance, obj_in=attendance_in)
    return attendance

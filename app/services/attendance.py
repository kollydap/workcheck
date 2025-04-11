# app/services/attendance.py
from typing import Any, Dict, Optional, List, Union
from datetime import datetime, date

from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.attendance import Attendance
from app.schemas.attendance import AttendanceCreate, AttendanceUpdate


async def get_attendance(
    db: AsyncSession, id: Optional[int] = None, skip: int = 0, limit: int = 100
) -> Union[Optional[Attendance], List[Attendance]]:
    if id:
        result = await db.execute(select(Attendance).filter(Attendance.id == id))
        return result.scalars().first()
    else:
        result = await db.execute(
            select(Attendance)
            .order_by(Attendance.check_in.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()


async def get_attendance_by_user(
    db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100
) -> List[Attendance]:
    result = await db.execute(
        select(Attendance)
        .filter(Attendance.user_id == user_id)
        .order_by(Attendance.check_in.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def get_attendance_by_date_range(
    db: AsyncSession,
    start_date: datetime,
    end_date: datetime,
    user_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
) -> List[Attendance]:
    query = select(Attendance).filter(
        and_(Attendance.check_in >= start_date, Attendance.check_in <= end_date)
    )

    if user_id:
        query = query.filter(Attendance.user_id == user_id)

    query = query.order_by(Attendance.check_in.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def get_user_current_status(
    db: AsyncSession, user_id: int
) -> Optional[Attendance]:
    """Get user's most recent attendance record for today"""
    today_start = datetime.combine(date.today(), datetime.min.time())
    today_end = datetime.combine(date.today(), datetime.max.time())

    result = await db.execute(
        select(Attendance)
        .filter(
            and_(
                Attendance.user_id == user_id,
                Attendance.check_in >= today_start,
                Attendance.check_in <= today_end,
            )
        )
        .order_by(Attendance.check_in.desc())
        .limit(1)
    )
    return result.scalars().first()


async def create_attendance(db: AsyncSession, obj_in: AttendanceCreate) -> Attendance:
    db_obj = Attendance(
        user_id=obj_in.user_id,
        check_in=obj_in.check_in,
        check_out=obj_in.check_out,
        latitude=obj_in.latitude,
        longitude=obj_in.longitude,
        check_in_method=obj_in.check_in_method,
        check_out_method=obj_in.check_out_method,
        notes=obj_in.notes,
    )
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def update_attendance(
    db: AsyncSession,
    db_obj: Attendance,
    obj_in: Union[AttendanceUpdate, Dict[str, Any]],
) -> Attendance:
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


async def check_in(
    db: AsyncSession,
    user_id: int,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    check_in_method: str = "MANUAL",
    notes: Optional[str] = None,
) -> Attendance:
    """User check-in"""
    attendance = Attendance(
        user_id=user_id,
        check_in=datetime.now(),
        latitude=latitude,
        longitude=longitude,
        check_in_method=check_in_method,
        notes=notes,
    )
    db.add(attendance)
    await db.commit()
    await db.refresh(attendance)
    return attendance


async def check_out(
    db: AsyncSession,
    attendance_id: int,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    check_out_method: str = "MANUAL",
    notes: Optional[str] = None,
) -> Attendance:
    """User check-out"""
    attendance = await get_attendance(db, id=attendance_id)

    # Update with check-out data
    attendance.check_out = datetime.now()
    attendance.check_out_method = check_out_method

    if latitude is not None:
        attendance.latitude = latitude
    if longitude is not None:
        attendance.longitude = longitude
    if notes:
        attendance.notes = (
            notes
            if not attendance.notes
            else f"{attendance.notes}\n\nCheck-out: {notes}"
        )

    db.add(attendance)
    await db.commit()
    await db.refresh(attendance)
    return attendance

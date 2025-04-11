# app/models/attendance.py
from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base


class Attendance(Base):
    __tablename__ = "attendance_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    check_in = Column(DateTime(timezone=True))
    check_out = Column(DateTime(timezone=True), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    check_in_method = Column(String)  # "QR", "NFC", "MANUAL"
    check_out_method = Column(String, nullable=True)  # "QR", "NFC", "MANUAL"
    notes = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="attendance_records")


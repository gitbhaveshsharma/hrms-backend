"""
Attendance Model

This module defines the Attendance SQLAlchemy model for the attendance table.
"""

from datetime import datetime, date
from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Index, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship, Mapped
from app.database import Base

if TYPE_CHECKING:
    from app.models.employee import Employee


class Attendance(Base):
    """
    Attendance database model.
    
    Represents an attendance record for an employee on a specific date.
    
    Attributes:
        id: Primary key (auto-increment)
        employee_id: Foreign key to employees table
        date: Date of attendance record
        status: Attendance status (Present/Absent)
        created_at: Timestamp when the record was created
        employee: Relationship to the Employee model
    """
    
    __tablename__ = "attendance"
    
    # Primary Key
    id: Mapped[int] = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )
    
    # Foreign Key to Employee
    employee_id: Mapped[int] = Column(
        Integer,
        ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Reference to the employee"
    )
    
    # Attendance Date
    date: Mapped[date] = Column(
        Date,
        nullable=False,
        comment="Date of attendance record"
    )
    
    # Attendance Status
    status: Mapped[str] = Column(
        String(20),
        nullable=False,
        comment="Attendance status: Present or Absent"
    )
    
    # Timestamps
    created_at: Mapped[datetime] = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        comment="Record creation timestamp"
    )
    
    # Relationships
    employee: Mapped["Employee"] = relationship(
        "Employee",
        back_populates="attendance_records"
    )
    
    # Table constraints and indexes
    __table_args__ = (
        # Unique constraint: one attendance record per employee per date
        UniqueConstraint(
            "employee_id",
            "date",
            name="uq_employee_date"
        ),
        # Check constraint for status values
        CheckConstraint(
            "status IN ('Present', 'Absent')",
            name="ck_attendance_status"
        ),
        # Index for date queries
        Index("ix_attendance_date", "date"),
        # Composite index for employee + date lookups
        Index("ix_attendance_employee_date", "employee_id", "date"),
    )
    
    def __repr__(self) -> str:
        """String representation of the Attendance object."""
        return f"<Attendance(id={self.id}, employee_id={self.employee_id}, date='{self.date}', status='{self.status}')>"
    
    def to_dict(self) -> dict:
        """
        Convert Attendance object to dictionary.
        
        Returns:
            dict: Dictionary representation of the attendance record
        """
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "date": self.date.isoformat() if self.date else None,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

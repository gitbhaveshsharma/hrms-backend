"""
Attendance Schemas

This module defines Pydantic schemas for attendance data validation.
"""

import datetime as dt
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, Field, field_validator


class AttendanceStatus(str, Enum):
    """
    Enum for attendance status values.
    """
    PRESENT = "Present"
    ABSENT = "Absent"


class AttendanceBase(BaseModel):
    """
    Base schema for Attendance with common fields.
    
    Attributes:
        employee_id: ID of the employee (database primary key)
        attendance_date: Date of attendance record
        status: Attendance status (Present/Absent)
    """
    
    employee_id: int = Field(
        ...,
        gt=0,
        description="Database ID of the employee",
        examples=[1, 2, 3]
    )
    
    attendance_date: dt.date = Field(
        ...,
        alias="date",
        description="Date of attendance (YYYY-MM-DD format)",
        examples=["2024-01-15", "2024-02-20"]
    )
    
    status: AttendanceStatus = Field(
        ...,
        description="Attendance status: Present or Absent",
        examples=["Present", "Absent"]
    )
    
    model_config = {"populate_by_name": True}
    
    @field_validator("attendance_date")
    @classmethod
    def validate_date_not_future(cls, value: dt.date) -> dt.date:
        """Validate that the date is not in the future."""
        if value > dt.date.today():
            raise ValueError("Attendance date cannot be in the future")
        return value
    
    @field_validator("status", mode="before")
    @classmethod
    def validate_status(cls, value: str) -> str:
        """Validate and normalize status value."""
        if isinstance(value, AttendanceStatus):
            return value
        
        value_str = str(value).strip().title()
        if value_str not in ["Present", "Absent"]:
            raise ValueError("Status must be 'Present' or 'Absent'")
        return value_str


class AttendanceCreate(AttendanceBase):
    """
    Schema for creating a new attendance record.
    
    Inherits all fields from AttendanceBase.
    """
    pass


class AttendanceResponse(BaseModel):
    """
    Schema for attendance response data.
    
    Includes all attendance fields plus related employee info.
    """
    
    id: int = Field(..., description="Database ID of the attendance record")
    employee_id: int = Field(..., description="Database ID of the employee")
    date: dt.date = Field(..., description="Date of attendance")
    status: str = Field(..., description="Attendance status")
    created_at: dt.datetime = Field(..., description="Record creation timestamp")
    
    # Optional employee details for enriched response
    employee_name: Optional[str] = Field(
        None,
        description="Name of the employee"
    )
    employee_code: Optional[str] = Field(
        None,
        description="Employee code"
    )
    
    model_config = {"from_attributes": True}


class AttendanceListResponse(BaseModel):
    """
    Schema for paginated attendance list response.
    """
    
    success: bool = Field(default=True, description="Request success status")
    data: List[AttendanceResponse] = Field(
        ...,
        description="List of attendance records"
    )
    total: int = Field(..., description="Total number of records")
    message: str = Field(
        default="Attendance records retrieved successfully",
        description="Response message"
    )


class AttendanceSummary(BaseModel):
    """
    Schema for attendance summary response.
    """
    
    employee_id: int = Field(..., description="Database ID of the employee")
    employee_name: str = Field(..., description="Name of the employee")
    total_days: int = Field(..., description="Total working days")
    present_days: int = Field(..., description="Days present")
    absent_days: int = Field(..., description="Days absent")
    attendance_percentage: float = Field(
        ...,
        description="Attendance percentage"
    )

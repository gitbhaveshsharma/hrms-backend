"""
Attendance Routes Module

This module defines API endpoints for attendance management.
"""

from typing import Dict, Any, Optional
from datetime import date
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.attendance import (
    AttendanceCreate,
    AttendanceResponse,
    AttendanceSummary
)
from app.services.attendance_service import AttendanceService

router = APIRouter(prefix="/api/attendance", tags=["Attendance"])


@router.post(
    "",
    response_model=Dict[str, Any],
    status_code=status.HTTP_201_CREATED,
    summary="Mark attendance",
    description="Mark attendance for an employee on a specific date."
)
def mark_attendance(
    attendance: AttendanceCreate,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Mark attendance for an employee.
    
    Args:
        attendance: Attendance data from request body
        db: Database session
        
    Returns:
        Dict containing success status and created attendance record
    """
    record = AttendanceService.mark_attendance(db, attendance)
    
    # Get employee details for enriched response
    employee = record.employee
    
    response_data = {
        "id": record.id,
        "employee_id": record.employee_id,
        "date": record.date.isoformat(),
        "status": record.status,
        "created_at": record.created_at.isoformat(),
        "employee_name": employee.full_name if employee else None,
        "employee_code": employee.employee_id if employee else None
    }
    
    return {
        "success": True,
        "data": response_data,
        "message": "Attendance marked successfully"
    }


@router.get(
    "",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Get all attendance records",
    description="Retrieve all attendance records with optional date filtering."
)
def get_all_attendance(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Max records to return"),
    date_filter: Optional[date] = Query(
        None,
        alias="date",
        description="Filter by specific date (YYYY-MM-DD)"
    ),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Retrieve all attendance records.
    
    Args:
        skip: Pagination offset
        limit: Maximum number of records
        date_filter: Optional date filter
        db: Database session
        
    Returns:
        Dict containing success status and list of attendance records
    """
    # Optimized: Use efficient count and join in single query
    from sqlalchemy import func
    from app.models.attendance import Attendance
    from app.models.employee import Employee
    
    if date_filter:
        records = AttendanceService.get_attendance_by_date(db, date_filter)
        total = len(records)
    else:
        # Get count efficiently
        total = db.query(func.count(Attendance.id)).scalar() or 0
        
        # Get records with employee names in single query
        records = (
            db.query(Attendance, Employee)
            .join(Employee, Attendance.employee_id == Employee.id)
            .order_by(Attendance.date.desc(), Attendance.id.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    # Format response
    if date_filter:
        # Old format for date filter (list of Attendance objects)
        pass  # Keep existing logic below
    else:
        # New optimized format
        return {
            "success": True,
            "data": [
                {
                    "id": record[0].id,
                    "employee_id": record[0].employee_id,
                    "date": record[0].date.isoformat(),
                    "status": record[0].status,
                    "created_at": record[0].created_at.isoformat(),
                    "employee_name": record[1].full_name,
                    "employee_code": record[1].employee_id
                }
                for record in records
            ],
            "total": total,
            "message": "Attendance records retrieved successfully"
        }
    
    # Original logic for date_filter case
    total = AttendanceService.get_attendance_count(db)
    
    response_data = []
    for record in records:
        employee = record.employee
        response_data.append({
            "id": record.id,
            "employee_id": record.employee_id,
            "date": record.date.isoformat(),
            "status": record.status,
            "created_at": record.created_at.isoformat(),
            "employee_name": employee.full_name if employee else None,
            "employee_code": employee.employee_id if employee else None
        })
    
    return {
        "success": True,
        "data": response_data,
        "total": total,
        "message": "Attendance records retrieved successfully"
    }


@router.get(
    "/employee/{employee_id}",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Get employee attendance",
    description="Retrieve all attendance records for a specific employee."
)
def get_employee_attendance(
    employee_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Retrieve attendance records for a specific employee.
    
    Args:
        employee_id: Database ID of the employee
        db: Database session
        
    Returns:
        Dict containing success status and list of attendance records
    """
    records = AttendanceService.get_attendance_by_employee(db, employee_id)
    
    response_data = []
    for record in records:
        employee = record.employee
        response_data.append({
            "id": record.id,
            "employee_id": record.employee_id,
            "date": record.date.isoformat(),
            "status": record.status,
            "created_at": record.created_at.isoformat(),
            "employee_name": employee.full_name if employee else None,
            "employee_code": employee.employee_id if employee else None
        })
    
    return {
        "success": True,
        "data": response_data,
        "total": len(response_data),
        "message": f"Attendance records for employee {employee_id} retrieved"
    }


@router.get(
    "/summary/{employee_id}",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Get attendance summary",
    description="Get attendance statistics summary for an employee."
)
def get_attendance_summary(
    employee_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get attendance summary statistics for an employee.
    
    Args:
        employee_id: Database ID of the employee
        db: Database session
        
    Returns:
        Dict containing attendance statistics
    """
    summary = AttendanceService.calculate_present_days(db, employee_id)
    
    return {
        "success": True,
        "data": summary,
        "message": "Attendance summary retrieved successfully"
    }

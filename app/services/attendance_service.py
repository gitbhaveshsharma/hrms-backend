"""
Attendance Service Module

This module contains business logic for attendance operations.
Implements the service layer pattern for separation of concerns.
"""

from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.attendance import Attendance
from app.models.employee import Employee
from app.schemas.attendance import AttendanceCreate
from app.utils.exceptions import (
    EmployeeNotFoundException,
    DuplicateAttendanceException,
    InvalidDateException
)


class AttendanceService:
    """
    Service class for attendance-related business logic.
    
    Provides methods for CRUD operations on attendance records
    with proper validation and error handling.
    """
    
    @staticmethod
    def mark_attendance(
        db: Session,
        attendance_data: AttendanceCreate
    ) -> Attendance:
        """
        Mark attendance for an employee on a specific date.
        
        Args:
            db: Database session
            attendance_data: Attendance data from request
            
        Returns:
            Attendance: Created attendance record
            
        Raises:
            EmployeeNotFoundException: If employee doesn't exist
            DuplicateAttendanceException: If attendance already marked
            InvalidDateException: If date is in the future
        """
        # Validate date is not in future
        if attendance_data.attendance_date > date.today():
            raise InvalidDateException(
                date=str(attendance_data.attendance_date),
                message="Cannot mark attendance for future dates"
            )
        
        # Validate employee exists
        employee = db.query(Employee).filter(
            Employee.id == attendance_data.employee_id
        ).first()
        
        if not employee:
            raise EmployeeNotFoundException(
                employee_id=attendance_data.employee_id
            )
        
        # Check for duplicate attendance
        existing = AttendanceService.check_duplicate_attendance(
            db,
            attendance_data.employee_id,
            attendance_data.attendance_date
        )
        
        if existing:
            raise DuplicateAttendanceException(
                employee_id=attendance_data.employee_id,
                date=str(attendance_data.attendance_date)
            )
        
        # Create attendance record
        db_attendance = Attendance(
            employee_id=attendance_data.employee_id,
            date=attendance_data.attendance_date,
            status=attendance_data.status.value
        )
        
        try:
            db.add(db_attendance)
            db.commit()
            db.refresh(db_attendance)
            return db_attendance
        except IntegrityError as e:
            db.rollback()
            raise DuplicateAttendanceException(
                employee_id=attendance_data.employee_id,
                date=str(attendance_data.attendance_date)
            )
    
    @staticmethod
    def check_duplicate_attendance(
        db: Session,
        employee_id: int,
        attendance_date: date
    ) -> Optional[Attendance]:
        """
        Check if attendance record exists for employee on date.
        
        Args:
            db: Database session
            employee_id: Employee database ID
            attendance_date: Date to check
            
        Returns:
            Optional[Attendance]: Existing record or None
        """
        return db.query(Attendance).filter(
            Attendance.employee_id == employee_id,
            Attendance.date == attendance_date
        ).first()
    
    @staticmethod
    def get_all_attendance_records(
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> List[Attendance]:
        """
        Retrieve all attendance records with pagination.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum records to return
            
        Returns:
            List[Attendance]: List of attendance records
        """
        return db.query(Attendance).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_attendance_count(db: Session) -> int:
        """
        Get total count of attendance records.
        
        Args:
            db: Database session
            
        Returns:
            int: Total number of attendance records
        """
        return db.query(Attendance).count()
    
    @staticmethod
    def get_attendance_by_employee(
        db: Session,
        employee_id: int
    ) -> List[Attendance]:
        """
        Get all attendance records for a specific employee.
        
        Args:
            db: Database session
            employee_id: Employee database ID
            
        Returns:
            List[Attendance]: List of attendance records
            
        Raises:
            EmployeeNotFoundException: If employee doesn't exist
        """
        # Validate employee exists
        employee = db.query(Employee).filter(
            Employee.id == employee_id
        ).first()
        
        if not employee:
            raise EmployeeNotFoundException(employee_id=employee_id)
        
        return db.query(Attendance).filter(
            Attendance.employee_id == employee_id
        ).order_by(Attendance.date.desc()).all()
    
    @staticmethod
    def get_attendance_by_date(
        db: Session,
        attendance_date: date
    ) -> List[Attendance]:
        """
        Get all attendance records for a specific date.
        
        Args:
            db: Database session
            attendance_date: Date to filter by
            
        Returns:
            List[Attendance]: List of attendance records for the date
        """
        return db.query(Attendance).filter(
            Attendance.date == attendance_date
        ).all()
    
    @staticmethod
    def get_attendance_by_date_range(
        db: Session,
        start_date: date,
        end_date: date,
        employee_id: Optional[int] = None
    ) -> List[Attendance]:
        """
        Get attendance records within a date range.
        
        Args:
            db: Database session
            start_date: Start of date range
            end_date: End of date range
            employee_id: Optional employee filter
            
        Returns:
            List[Attendance]: List of attendance records
        """
        query = db.query(Attendance).filter(
            Attendance.date >= start_date,
            Attendance.date <= end_date
        )
        
        if employee_id:
            query = query.filter(Attendance.employee_id == employee_id)
        
        return query.order_by(Attendance.date.desc()).all()
    
    @staticmethod
    def calculate_present_days(db: Session, employee_id: int) -> dict:
        """
        Calculate attendance statistics for an employee.
        
        Args:
            db: Database session
            employee_id: Employee database ID
            
        Returns:
            dict: Attendance statistics
            
        Raises:
            EmployeeNotFoundException: If employee doesn't exist
        """
        # Validate employee exists
        employee = db.query(Employee).filter(
            Employee.id == employee_id
        ).first()
        
        if not employee:
            raise EmployeeNotFoundException(employee_id=employee_id)
        
        # Get all attendance records
        records = db.query(Attendance).filter(
            Attendance.employee_id == employee_id
        ).all()
        
        total_days = len(records)
        present_days = sum(1 for r in records if r.status == "Present")
        absent_days = total_days - present_days
        
        attendance_percentage = 0.0
        if total_days > 0:
            attendance_percentage = round((present_days / total_days) * 100, 2)
        
        return {
            "employee_id": employee_id,
            "employee_name": employee.full_name,
            "total_days": total_days,
            "present_days": present_days,
            "absent_days": absent_days,
            "attendance_percentage": attendance_percentage
        }
    
    @staticmethod
    def validate_employee_exists(db: Session, employee_id: int) -> bool:
        """
        Validate that an employee exists in the database.
        
        Args:
            db: Database session
            employee_id: Employee database ID
            
        Returns:
            bool: True if employee exists
            
        Raises:
            EmployeeNotFoundException: If employee doesn't exist
        """
        employee = db.query(Employee).filter(
            Employee.id == employee_id
        ).first()
        
        if not employee:
            raise EmployeeNotFoundException(employee_id=employee_id)
        
        return True

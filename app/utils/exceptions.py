"""
Custom Exceptions Module

This module defines custom exception classes for the HRMS Lite application.
These exceptions provide meaningful error messages and appropriate HTTP status codes.
"""

from typing import Optional, Dict, Any


class HRMSException(Exception):
    """
    Base exception class for HRMS Lite application.
    
    All custom exceptions should inherit from this class.
    
    Attributes:
        message: Human-readable error message
        status_code: HTTP status code for the error
        details: Additional error details
    """
    
    def __init__(
        self,
        message: str = "An error occurred",
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Initialize the HRMS exception.
        
        Args:
            message: Human-readable error message
            status_code: HTTP status code
            details: Additional error details
        """
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert exception to dictionary format.
        
        Returns:
            Dict containing error information
        """
        return {
            "success": False,
            "error": self.message,
            "status_code": self.status_code,
            "details": self.details
        }


class EmployeeNotFoundException(HRMSException):
    """
    Exception raised when an employee is not found.
    
    Used when attempting to retrieve, update, or delete
    an employee that doesn't exist in the database.
    """
    
    def __init__(
        self,
        employee_id: Optional[int] = None,
        message: Optional[str] = None
    ) -> None:
        """
        Initialize the EmployeeNotFoundException.
        
        Args:
            employee_id: ID of the employee that was not found
            message: Custom error message
        """
        if message is None:
            if employee_id:
                message = f"Employee with ID {employee_id} not found"
            else:
                message = "Employee not found"
        
        super().__init__(
            message=message,
            status_code=404,
            details={"employee_id": employee_id} if employee_id else {}
        )


class DuplicateEmployeeException(HRMSException):
    """
    Exception raised when attempting to create a duplicate employee.
    
    Used when an employee with the same employee_id or email
    already exists in the database.
    """
    
    def __init__(
        self,
        field: str = "employee_id",
        value: Optional[str] = None,
        message: Optional[str] = None
    ) -> None:
        """
        Initialize the DuplicateEmployeeException.
        
        Args:
            field: The field that has a duplicate value
            value: The duplicate value
            message: Custom error message
        """
        if message is None:
            if value:
                message = f"Employee with {field} '{value}' already exists"
            else:
                message = f"Employee with this {field} already exists"
        
        super().__init__(
            message=message,
            status_code=409,
            details={"field": field, "value": value}
        )


class DuplicateAttendanceException(HRMSException):
    """
    Exception raised when attempting to create duplicate attendance.
    
    Used when an attendance record for the same employee and date
    already exists in the database.
    """
    
    def __init__(
        self,
        employee_id: Optional[int] = None,
        date: Optional[str] = None,
        message: Optional[str] = None
    ) -> None:
        """
        Initialize the DuplicateAttendanceException.
        
        Args:
            employee_id: ID of the employee
            date: Date of the attendance record
            message: Custom error message
        """
        if message is None:
            if employee_id and date:
                message = f"Attendance for employee {employee_id} on {date} already exists"
            else:
                message = "Attendance record for this employee and date already exists"
        
        super().__init__(
            message=message,
            status_code=409,
            details={"employee_id": employee_id, "date": date}
        )


class InvalidDateException(HRMSException):
    """
    Exception raised when an invalid date is provided.
    
    Used when the date is in an invalid format or is a future date.
    """
    
    def __init__(
        self,
        date: Optional[str] = None,
        message: Optional[str] = None
    ) -> None:
        """
        Initialize the InvalidDateException.
        
        Args:
            date: The invalid date value
            message: Custom error message
        """
        if message is None:
            if date:
                message = f"Invalid date: {date}. Date cannot be in the future."
            else:
                message = "Invalid date provided"
        
        super().__init__(
            message=message,
            status_code=400,
            details={"date": date} if date else {}
        )


class ValidationException(HRMSException):
    """
    Exception raised for general validation errors.
    
    Used for input validation failures that don't fit other categories.
    """
    
    def __init__(
        self,
        message: str = "Validation error",
        field: Optional[str] = None,
        value: Optional[Any] = None
    ) -> None:
        """
        Initialize the ValidationException.
        
        Args:
            message: Error message describing the validation failure
            field: The field that failed validation
            value: The invalid value
        """
        details = {}
        if field:
            details["field"] = field
        if value is not None:
            details["value"] = str(value)
        
        super().__init__(
            message=message,
            status_code=400,
            details=details
        )

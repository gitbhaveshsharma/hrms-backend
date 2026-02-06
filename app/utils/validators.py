"""
Validators Module

This module contains utility validation functions for the HRMS Lite application.
These functions are used throughout the application for input validation.
"""

import re
from datetime import date
from typing import Optional


def validate_email_format(email: str) -> bool:
    """
    Validate email format using regex pattern.
    
    Args:
        email: Email address to validate
        
    Returns:
        bool: True if email format is valid, False otherwise
        
    Example:
        >>> validate_email_format("john.doe@company.com")
        True
        >>> validate_email_format("invalid-email")
        False
    """
    if not email or not isinstance(email, str):
        return False
    
    email = email.strip().lower()
    
    # RFC 5322 compliant email regex pattern
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    
    return bool(re.match(email_pattern, email))


def validate_date_not_future(check_date: date) -> bool:
    """
    Validate that the given date is not in the future.
    
    Args:
        check_date: Date to validate
        
    Returns:
        bool: True if date is not in the future, False otherwise
        
    Example:
        >>> from datetime import date
        >>> validate_date_not_future(date(2024, 1, 1))
        True
        >>> validate_date_not_future(date(2099, 1, 1))
        False
    """
    if not check_date or not isinstance(check_date, date):
        return False
    
    return check_date <= date.today()


def validate_status_enum(status: str) -> bool:
    """
    Validate that the status is a valid attendance status.
    
    Args:
        status: Status value to validate
        
    Returns:
        bool: True if status is valid (Present/Absent), False otherwise
        
    Example:
        >>> validate_status_enum("Present")
        True
        >>> validate_status_enum("Late")
        False
    """
    if not status or not isinstance(status, str):
        return False
    
    valid_statuses = ["Present", "Absent"]
    return status.strip().title() in valid_statuses


def validate_non_empty_string(value: str, min_length: int = 1) -> bool:
    """
    Validate that a string is not empty and meets minimum length.
    
    Args:
        value: String value to validate
        min_length: Minimum required length (default: 1)
        
    Returns:
        bool: True if string is valid, False otherwise
    """
    if not value or not isinstance(value, str):
        return False
    
    return len(value.strip()) >= min_length


def validate_employee_id_format(employee_id: str) -> bool:
    """
    Validate employee ID format.
    
    Employee ID should be alphanumeric and not empty.
    
    Args:
        employee_id: Employee ID to validate
        
    Returns:
        bool: True if format is valid, False otherwise
        
    Example:
        >>> validate_employee_id_format("EMP001")
        True
        >>> validate_employee_id_format("")
        False
    """
    if not employee_id or not isinstance(employee_id, str):
        return False
    
    employee_id = employee_id.strip()
    if not employee_id:
        return False
    
    # Allow alphanumeric characters, hyphens, and underscores
    pattern = r"^[a-zA-Z0-9_-]+$"
    return bool(re.match(pattern, employee_id))


def sanitize_string(value: Optional[str]) -> Optional[str]:
    """
    Sanitize a string by stripping whitespace.
    
    Args:
        value: String to sanitize
        
    Returns:
        Sanitized string or None if input is None
    """
    if value is None:
        return None
    
    if not isinstance(value, str):
        return str(value).strip()
    
    return value.strip()


def validate_positive_integer(value: int) -> bool:
    """
    Validate that a value is a positive integer.
    
    Args:
        value: Integer to validate
        
    Returns:
        bool: True if value is a positive integer, False otherwise
    """
    if not isinstance(value, int):
        return False
    
    return value > 0

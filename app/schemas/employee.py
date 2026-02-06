"""
Employee Schemas

This module defines Pydantic schemas for employee data validation.
"""

import re
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator, EmailStr


class EmployeeBase(BaseModel):
    """
    Base schema for Employee with common fields.
    
    Attributes:
        employee_id: Unique identifier for the employee
        full_name: Full name of the employee
        email: Email address of the employee
        department: Department name
    """
    
    employee_id: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Unique employee identifier (e.g., EMP001)",
        examples=["EMP001", "HR002"]
    )
    
    full_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Full name of the employee",
        examples=["John Doe", "Jane Smith"]
    )
    
    email: str = Field(
        ...,
        max_length=255,
        description="Email address of the employee",
        examples=["john.doe@company.com"]
    )
    
    department: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Department name",
        examples=["Engineering", "Human Resources", "Finance"]
    )
    
    @field_validator("employee_id")
    @classmethod
    def validate_employee_id(cls, value: str) -> str:
        """Validate and clean employee_id."""
        value = value.strip()
        if not value:
            raise ValueError("Employee ID cannot be empty")
        return value
    
    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value: str) -> str:
        """Validate and clean full_name."""
        value = value.strip()
        if not value:
            raise ValueError("Full name cannot be empty")
        if len(value) < 2:
            raise ValueError("Full name must be at least 2 characters")
        return value
    
    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        """Validate email format using regex."""
        value = value.strip().lower()
        if not value:
            raise ValueError("Email cannot be empty")
        
        # Email validation regex pattern
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_pattern, value):
            raise ValueError("Invalid email format")
        
        return value
    
    @field_validator("department")
    @classmethod
    def validate_department(cls, value: str) -> str:
        """Validate and clean department."""
        value = value.strip()
        if not value:
            raise ValueError("Department cannot be empty")
        return value


class EmployeeCreate(EmployeeBase):
    """
    Schema for creating a new employee.
    
    Inherits all fields from EmployeeBase.
    """
    pass


class EmployeeUpdate(BaseModel):
    """
    Schema for updating an existing employee.
    
    All fields are optional to allow partial updates.
    """
    
    full_name: Optional[str] = Field(
        None,
        min_length=2,
        max_length=100,
        description="Full name of the employee"
    )
    
    email: Optional[str] = Field(
        None,
        max_length=255,
        description="Email address of the employee"
    )
    
    department: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Department name"
    )
    
    @field_validator("email")
    @classmethod
    def validate_email(cls, value: Optional[str]) -> Optional[str]:
        """Validate email format if provided."""
        if value is None:
            return value
        
        value = value.strip().lower()
        if not value:
            return None
        
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_pattern, value):
            raise ValueError("Invalid email format")
        
        return value


class EmployeeResponse(EmployeeBase):
    """
    Schema for employee response data.
    
    Includes all base fields plus id and timestamps.
    """
    
    id: int = Field(..., description="Database ID of the employee")
    created_at: datetime = Field(..., description="Record creation timestamp")
    updated_at: datetime = Field(..., description="Record last update timestamp")
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True


class EmployeeListResponse(BaseModel):
    """
    Schema for paginated employee list response.
    """
    
    success: bool = Field(default=True, description="Request success status")
    data: List[EmployeeResponse] = Field(..., description="List of employees")
    total: int = Field(..., description="Total number of employees")
    message: str = Field(
        default="Employees retrieved successfully",
        description="Response message"
    )

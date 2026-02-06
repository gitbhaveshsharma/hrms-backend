"""
Employee Routes Module

This module defines API endpoints for employee management.
"""

from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.employee import (
    EmployeeCreate,
    EmployeeResponse,
    EmployeeListResponse
)
from app.services.employee_service import EmployeeService
from app.utils.exceptions import (
    EmployeeNotFoundException,
    DuplicateEmployeeException
)

router = APIRouter(prefix="/api/employees", tags=["Employees"])


@router.post(
    "",
    response_model=Dict[str, Any],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new employee",
    description="Create a new employee record with unique employee_id and email."
)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Create a new employee in the HRMS system.
    
    Args:
        employee: Employee data from request body
        db: Database session
        
    Returns:
        Dict containing success status and created employee data
    """
    created_employee = EmployeeService.create_employee(db, employee)
    
    return {
        "success": True,
        "data": EmployeeResponse.model_validate(created_employee).model_dump(),
        "message": "Employee created successfully"
    }


@router.get(
    "",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Get all employees",
    description="Retrieve a list of all employees with optional pagination."
)
def get_all_employees(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Max records to return"),
    department: Optional[str] = Query(None, description="Filter by department"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Retrieve all employees from the database.
    
    Args:
        skip: Pagination offset
        limit: Maximum number of records
        department: Optional department filter
        db: Database session
        
    Returns:
        Dict containing success status and list of employees
    """
    # Optimized: Get count efficiently with func.count
    from sqlalchemy import func
    from app.models.employee import Employee
    
    if department:
        employees = EmployeeService.search_employees(db, department=department)
        total = len(employees)
    else:
        # Get count efficiently
        total = db.query(func.count(Employee.id)).scalar() or 0
        employees = (
            db.query(Employee)
            .order_by(Employee.id.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    return {
        "success": True,
        "data": [
            EmployeeResponse.model_validate(emp).model_dump()
            for emp in employees
        ],
        "total": total,
        "message": "Employees retrieved successfully"
    }


@router.get(
    "/{employee_id}",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Get employee by ID",
    description="Retrieve a specific employee by their database ID."
)
def get_employee_by_id(
    employee_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Retrieve a single employee by their database ID.
    
    Args:
        employee_id: Database primary key ID
        db: Database session
        
    Returns:
        Dict containing success status and employee data
    """
    employee = EmployeeService.get_employee_by_id(db, employee_id)
    
    return {
        "success": True,
        "data": EmployeeResponse.model_validate(employee).model_dump(),
        "message": "Employee retrieved successfully"
    }


@router.delete(
    "/{employee_id}",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Delete an employee",
    description="Delete an employee and cascade to related attendance records."
)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Delete an employee by their database ID.
    
    This will also delete all associated attendance records.
    
    Args:
        employee_id: Database primary key ID
        db: Database session
        
    Returns:
        Dict containing success status and confirmation message
    """
    EmployeeService.delete_employee(db, employee_id)
    
    return {
        "success": True,
        "data": None,
        "message": f"Employee with ID {employee_id} deleted successfully"
    }

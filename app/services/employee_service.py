"""
Employee Service Module

This module contains business logic for employee operations.
Implements the service layer pattern for separation of concerns.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from app.utils.exceptions import (
    EmployeeNotFoundException,
    DuplicateEmployeeException
)


class EmployeeService:
    """
    Service class for employee-related business logic.
    
    Provides methods for CRUD operations on employees with
    proper validation and error handling.
    """
    
    @staticmethod
    def create_employee(db: Session, employee_data: EmployeeCreate) -> Employee:
        """
        Create a new employee record.
        
        Args:
            db: Database session
            employee_data: Employee data from request
            
        Returns:
            Employee: Created employee object
            
        Raises:
            DuplicateEmployeeException: If employee_id or email already exists
        """
        # Check for duplicate employee_id
        if EmployeeService.get_employee_by_employee_id(db, employee_data.employee_id):
            raise DuplicateEmployeeException(
                field="employee_id",
                value=employee_data.employee_id
            )
        
        # Check for duplicate email
        if EmployeeService.get_employee_by_email(db, employee_data.email):
            raise DuplicateEmployeeException(
                field="email",
                value=employee_data.email
            )
        
        # Create new employee
        db_employee = Employee(
            employee_id=employee_data.employee_id,
            full_name=employee_data.full_name,
            email=employee_data.email.lower(),
            department=employee_data.department
        )
        
        try:
            db.add(db_employee)
            db.commit()
            db.refresh(db_employee)
            return db_employee
        except IntegrityError as e:
            db.rollback()
            raise DuplicateEmployeeException(
                message="Employee with this ID or email already exists"
            )
    
    @staticmethod
    def get_all_employees(
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> List[Employee]:
        """
        Retrieve all employees with optional pagination.
        
        Args:
            db: Database session
            skip: Number of records to skip (offset)
            limit: Maximum number of records to return
            
        Returns:
            List[Employee]: List of employee objects
        """
        return db.query(Employee).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_employee_count(db: Session) -> int:
        """
        Get total count of employees.
        
        Args:
            db: Database session
            
        Returns:
            int: Total number of employees
        """
        return db.query(Employee).count()
    
    @staticmethod
    def get_employee_by_id(db: Session, employee_id: int) -> Employee:
        """
        Retrieve an employee by database ID.
        
        Args:
            db: Database session
            employee_id: Database primary key ID
            
        Returns:
            Employee: Employee object
            
        Raises:
            EmployeeNotFoundException: If employee not found
        """
        employee = db.query(Employee).filter(Employee.id == employee_id).first()
        
        if not employee:
            raise EmployeeNotFoundException(employee_id=employee_id)
        
        return employee
    
    @staticmethod
    def get_employee_by_employee_id(
        db: Session,
        employee_id: str
    ) -> Optional[Employee]:
        """
        Retrieve an employee by employee_id (e.g., EMP001).
        
        Args:
            db: Database session
            employee_id: Unique employee identifier
            
        Returns:
            Optional[Employee]: Employee object or None if not found
        """
        return db.query(Employee).filter(
            Employee.employee_id == employee_id
        ).first()
    
    @staticmethod
    def get_employee_by_email(db: Session, email: str) -> Optional[Employee]:
        """
        Retrieve an employee by email address.
        
        Args:
            db: Database session
            email: Employee email address
            
        Returns:
            Optional[Employee]: Employee object or None if not found
        """
        return db.query(Employee).filter(
            Employee.email == email.lower()
        ).first()
    
    @staticmethod
    def update_employee(
        db: Session,
        employee_id: int,
        employee_data: EmployeeUpdate
    ) -> Employee:
        """
        Update an existing employee.
        
        Args:
            db: Database session
            employee_id: Database primary key ID
            employee_data: Updated employee data
            
        Returns:
            Employee: Updated employee object
            
        Raises:
            EmployeeNotFoundException: If employee not found
            DuplicateEmployeeException: If email already exists
        """
        employee = EmployeeService.get_employee_by_id(db, employee_id)
        
        # Check for email conflict if email is being updated
        if employee_data.email:
            existing = EmployeeService.get_employee_by_email(db, employee_data.email)
            if existing and existing.id != employee_id:
                raise DuplicateEmployeeException(
                    field="email",
                    value=employee_data.email
                )
        
        # Update fields if provided
        update_data = employee_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if value is not None:
                setattr(employee, field, value)
        
        try:
            db.commit()
            db.refresh(employee)
            return employee
        except IntegrityError:
            db.rollback()
            raise DuplicateEmployeeException(
                message="Email already exists"
            )
    
    @staticmethod
    def delete_employee(db: Session, employee_id: int) -> bool:
        """
        Delete an employee by ID.
        
        Cascades deletion to related attendance records.
        
        Args:
            db: Database session
            employee_id: Database primary key ID
            
        Returns:
            bool: True if deleted successfully
            
        Raises:
            EmployeeNotFoundException: If employee not found
        """
        employee = EmployeeService.get_employee_by_id(db, employee_id)
        
        db.delete(employee)
        db.commit()
        
        return True
    
    @staticmethod
    def search_employees(
        db: Session,
        department: Optional[str] = None,
        name: Optional[str] = None
    ) -> List[Employee]:
        """
        Search employees by department or name.
        
        Args:
            db: Database session
            department: Department to filter by
            name: Name pattern to search
            
        Returns:
            List[Employee]: List of matching employees
        """
        query = db.query(Employee)
        
        if department:
            query = query.filter(Employee.department == department)
        
        if name:
            query = query.filter(Employee.full_name.ilike(f"%{name}%"))
        
        return query.all()

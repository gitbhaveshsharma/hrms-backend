"""
Employee Model

This module defines the Employee SQLAlchemy model for the employees table.
"""

from datetime import datetime
from typing import TYPE_CHECKING, List
from sqlalchemy import Column, Integer, String, DateTime, Index
from sqlalchemy.orm import relationship, Mapped
from app.database import Base

if TYPE_CHECKING:
    from app.models.attendance import Attendance


class Employee(Base):
    """
    Employee database model.
    
    Represents an employee in the HRMS system with personal details
    and department information.
    
    Attributes:
        id: Primary key (auto-increment)
        employee_id: Unique identifier for the employee (e.g., EMP001)
        full_name: Full name of the employee
        email: Unique email address of the employee
        department: Department where the employee works
        created_at: Timestamp when the record was created
        updated_at: Timestamp when the record was last updated
        attendance_records: Relationship to attendance records
    """
    
    __tablename__ = "employees"
    
    # Primary Key
    id: Mapped[int] = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )
    
    # Employee Identification
    employee_id: Mapped[str] = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
        comment="Unique employee identifier (e.g., EMP001)"
    )
    
    # Personal Information
    full_name: Mapped[str] = Column(
        String(100),
        nullable=False,
        comment="Full name of the employee"
    )
    
    email: Mapped[str] = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
        comment="Email address of the employee"
    )
    
    # Department Information
    department: Mapped[str] = Column(
        String(100),
        nullable=False,
        comment="Department name"
    )
    
    # Timestamps
    created_at: Mapped[datetime] = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        comment="Record creation timestamp"
    )
    
    updated_at: Mapped[datetime] = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        comment="Record last update timestamp"
    )
    
    # Relationships
    attendance_records: Mapped[List["Attendance"]] = relationship(
        "Attendance",
        back_populates="employee",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    # Table indexes for optimization
    __table_args__ = (
        Index("ix_employees_department", "department"),
        Index("ix_employees_full_name", "full_name"),
    )
    
    def __repr__(self) -> str:
        """String representation of the Employee object."""
        return f"<Employee(id={self.id}, employee_id='{self.employee_id}', name='{self.full_name}')>"
    
    def to_dict(self) -> dict:
        """
        Convert Employee object to dictionary.
        
        Returns:
            dict: Dictionary representation of the employee
        """
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "full_name": self.full_name,
            "email": self.email,
            "department": self.department,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

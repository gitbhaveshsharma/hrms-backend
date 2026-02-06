"""Create employees table

Revision ID: 001
Revises: 
Create Date: 2024-01-15 10:00:00.000000

This migration creates the employees table with all necessary columns,
constraints, and indexes for the HRMS Lite application.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Create the employees table.
    
    Table Structure:
    - id: Primary key (auto-increment)
    - employee_id: Unique identifier (e.g., EMP001)
    - full_name: Employee's full name
    - email: Unique email address
    - department: Department name
    - created_at: Record creation timestamp
    - updated_at: Record last update timestamp
    
    Indexes:
    - Primary key on id
    - Unique index on employee_id
    - Unique index on email
    - Index on department for filtering
    - Index on full_name for searching
    """
    op.create_table(
        'employees',
        
        # Primary Key
        sa.Column(
            'id',
            sa.Integer(),
            autoincrement=True,
            nullable=False,
            primary_key=True,
            comment='Primary key'
        ),
        
        # Employee Identification
        sa.Column(
            'employee_id',
            sa.String(length=50),
            nullable=False,
            unique=True,
            comment='Unique employee identifier (e.g., EMP001)'
        ),
        
        # Personal Information
        sa.Column(
            'full_name',
            sa.String(length=100),
            nullable=False,
            comment='Full name of the employee'
        ),
        
        sa.Column(
            'email',
            sa.String(length=255),
            nullable=False,
            unique=True,
            comment='Email address of the employee'
        ),
        
        # Department
        sa.Column(
            'department',
            sa.String(length=100),
            nullable=False,
            comment='Department name'
        ),
        
        # Timestamps
        sa.Column(
            'created_at',
            sa.DateTime(),
            nullable=False,
            server_default=sa.text('CURRENT_TIMESTAMP'),
            comment='Record creation timestamp'
        ),
        
        sa.Column(
            'updated_at',
            sa.DateTime(),
            nullable=False,
            server_default=sa.text('CURRENT_TIMESTAMP'),
            comment='Record last update timestamp'
        ),
    )
    
    # Create indexes for better query performance
    op.create_index(
        'ix_employees_id',
        'employees',
        ['id'],
        unique=False
    )
    
    op.create_index(
        'ix_employees_employee_id',
        'employees',
        ['employee_id'],
        unique=True
    )
    
    op.create_index(
        'ix_employees_email',
        'employees',
        ['email'],
        unique=True
    )
    
    op.create_index(
        'ix_employees_department',
        'employees',
        ['department'],
        unique=False
    )
    
    op.create_index(
        'ix_employees_full_name',
        'employees',
        ['full_name'],
        unique=False
    )


def downgrade() -> None:
    """
    Drop the employees table and all its indexes.
    
    This will also cascade delete any related attendance records
    due to the foreign key constraint in the attendance table.
    """
    # Drop indexes first
    op.drop_index('ix_employees_full_name', table_name='employees')
    op.drop_index('ix_employees_department', table_name='employees')
    op.drop_index('ix_employees_email', table_name='employees')
    op.drop_index('ix_employees_employee_id', table_name='employees')
    op.drop_index('ix_employees_id', table_name='employees')
    
    # Drop the table
    op.drop_table('employees')

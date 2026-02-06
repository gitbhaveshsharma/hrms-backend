"""Create attendance table

Revision ID: 002
Revises: 001
Create Date: 2024-01-15 10:30:00.000000

This migration creates the attendance table with foreign key relationship
to the employees table, unique constraints, and check constraints.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Create the attendance table.
    
    Table Structure:
    - id: Primary key (auto-increment)
    - employee_id: Foreign key to employees table
    - date: Date of attendance record
    - status: Attendance status (Present/Absent)
    - created_at: Record creation timestamp
    
    Constraints:
    - Foreign key to employees table with CASCADE delete
    - Unique constraint on (employee_id, date) combination
    - Check constraint for status values
    
    Indexes:
    - Primary key on id
    - Index on employee_id for foreign key lookups
    - Index on date for date-based queries
    - Composite index on (employee_id, date)
    """
    op.create_table(
        'attendance',
        
        # Primary Key
        sa.Column(
            'id',
            sa.Integer(),
            autoincrement=True,
            nullable=False,
            primary_key=True,
            comment='Primary key'
        ),
        
        # Foreign Key to Employees
        sa.Column(
            'employee_id',
            sa.Integer(),
            sa.ForeignKey('employees.id', ondelete='CASCADE'),
            nullable=False,
            comment='Reference to the employee'
        ),
        
        # Attendance Date
        sa.Column(
            'date',
            sa.Date(),
            nullable=False,
            comment='Date of attendance record'
        ),
        
        # Attendance Status
        sa.Column(
            'status',
            sa.String(length=20),
            nullable=False,
            comment='Attendance status: Present or Absent'
        ),
        
        # Timestamps
        sa.Column(
            'created_at',
            sa.DateTime(),
            nullable=False,
            server_default=sa.text('CURRENT_TIMESTAMP'),
            comment='Record creation timestamp'
        ),
    )
    
    # Create unique constraint on (employee_id, date) combination
    op.create_unique_constraint(
        'uq_employee_date',
        'attendance',
        ['employee_id', 'date']
    )
    
    # Create check constraint for status values
    op.create_check_constraint(
        'ck_attendance_status',
        'attendance',
        "status IN ('Present', 'Absent')"
    )
    
    # Create indexes for better query performance
    op.create_index(
        'ix_attendance_id',
        'attendance',
        ['id'],
        unique=False
    )
    
    op.create_index(
        'ix_attendance_employee_id',
        'attendance',
        ['employee_id'],
        unique=False
    )
    
    op.create_index(
        'ix_attendance_date',
        'attendance',
        ['date'],
        unique=False
    )
    
    op.create_index(
        'ix_attendance_employee_date',
        'attendance',
        ['employee_id', 'date'],
        unique=False
    )


def downgrade() -> None:
    """
    Drop the attendance table and all its constraints and indexes.
    """
    # Drop indexes first
    op.drop_index('ix_attendance_employee_date', table_name='attendance')
    op.drop_index('ix_attendance_date', table_name='attendance')
    op.drop_index('ix_attendance_employee_id', table_name='attendance')
    op.drop_index('ix_attendance_id', table_name='attendance')
    
    # Drop constraints
    op.drop_constraint('ck_attendance_status', 'attendance', type_='check')
    op.drop_constraint('uq_employee_date', 'attendance', type_='unique')
    
    # Drop the table
    op.drop_table('attendance')

"""
Seed Data Script for HRMS Lite

This script populates the database with sample data including Indian names.
Run this script to add test data to your database.
"""

from datetime import date, timedelta
import random
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models.employee import Employee
from app.models.attendance import Attendance
from app.database import Base

# Sample Indian names
INDIAN_NAMES = [
    ("Rajesh Kumar", "rajesh.kumar@company.com", "Engineering"),
    ("Priya Sharma", "priya.sharma@company.com", "Human Resources"),
    ("Amit Patel", "amit.patel@company.com", "Finance"),
    ("Sneha Reddy", "sneha.reddy@company.com", "Marketing"),
    ("Vikram Singh", "vikram.singh@company.com", "Engineering"),
    ("Ananya Iyer", "ananya.iyer@company.com", "Product Management"),
    ("Arjun Verma", "arjun.verma@company.com", "Engineering"),
    ("Kavya Nair", "kavya.nair@company.com", "Design"),
    ("Rahul Gupta", "rahul.gupta@company.com", "Sales"),
    ("Meera Joshi", "meera.joshi@company.com", "Operations"),
    ("Aditya Rao", "aditya.rao@company.com", "Engineering"),
    ("Divya Menon", "divya.menon@company.com", "Quality Assurance"),
    ("Rohan Desai", "rohan.desai@company.com", "Customer Support"),
    ("Pooja Kapoor", "pooja.kapoor@company.com", "Human Resources"),
    ("Sanjay Pillai", "sanjay.pillai@company.com", "Finance"),
    ("Neha Agarwal", "neha.agarwal@company.com", "Marketing"),
    ("Karthik Krishnan", "karthik.krishnan@company.com", "Engineering"),
    ("Riya Bhatia", "riya.bhatia@company.com", "Business Development"),
    ("Manish Saxena", "manish.saxena@company.com", "IT Support"),
    ("Tanvi Malhotra", "tanvi.malhotra@company.com", "Legal"),
]


def clear_existing_data(db: Session) -> None:
    """Clear all existing data from tables."""
    print("Clearing existing data...")
    db.query(Attendance).delete()
    db.query(Employee).delete()
    db.commit()
    print("✓ Existing data cleared")


def create_employees(db: Session) -> list:
    """Create employee records."""
    print("\nCreating employees...")
    employees = []
    
    for idx, (name, email, department) in enumerate(INDIAN_NAMES, start=1):
        employee = Employee(
            employee_id=f"EMP{idx:03d}",
            full_name=name,
            email=email,
            department=department
        )
        db.add(employee)
        employees.append(employee)
        print(f"  Added: {name} ({employee.employee_id})")
    
    db.commit()
    print(f"✓ Created {len(employees)} employees")
    return employees


def create_attendance_records(db: Session, employees: list) -> None:
    """Create attendance records for the last 30 days."""
    print("\nCreating attendance records...")
    
    # Generate attendance for last 30 days
    start_date = date.today() - timedelta(days=30)
    total_records = 0
    
    for employee in employees:
        # Refresh employee to get the ID
        db.refresh(employee)
        
        for day in range(30):
            attendance_date = start_date + timedelta(days=day)
            
            # Skip weekends (Saturday=5, Sunday=6)
            if attendance_date.weekday() >= 5:
                continue
            
            # 90% present, 10% absent (random)
            status = "Present" if random.random() < 0.9 else "Absent"
            
            attendance = Attendance(
                employee_id=employee.id,
                date=attendance_date,
                status=status
            )
            db.add(attendance)
            total_records += 1
    
    db.commit()
    print(f"✓ Created {total_records} attendance records")


def verify_data(db: Session) -> None:
    """Verify the seeded data."""
    print("\n" + "="*50)
    print("DATA VERIFICATION")
    print("="*50)
    
    employee_count = db.query(Employee).count()
    attendance_count = db.query(Attendance).count()
    
    print(f"Total Employees: {employee_count}")
    print(f"Total Attendance Records: {attendance_count}")
    
    # Show sample employees by department
    print("\nEmployees by Department:")
    departments = db.query(Employee.department).distinct().all()
    for (dept,) in departments:
        count = db.query(Employee).filter(Employee.department == dept).count()
        print(f"  {dept}: {count} employees")
    
    # Show recent attendance
    print("\nRecent Attendance Summary:")
    recent_date = date.today() - timedelta(days=1)
    present_count = db.query(Attendance).filter(
        Attendance.date == recent_date,
        Attendance.status == "Present"
    ).count()
    absent_count = db.query(Attendance).filter(
        Attendance.date == recent_date,
        Attendance.status == "Absent"
    ).count()
    
    print(f"  Date: {recent_date}")
    print(f"  Present: {present_count}")
    print(f"  Absent: {absent_count}")
    
    print("\n" + "="*50)


def seed_database():
    """Main function to seed the database."""
    print("\n" + "="*50)
    print("HRMS LITE - DATABASE SEEDING")
    print("="*50)
    
    db = SessionLocal()
    
    try:
        # Clear existing data
        clear_existing_data(db)
        
        # Create employees
        employees = create_employees(db)
        
        # Create attendance records
        create_attendance_records(db, employees)
        
        # Verify data
        verify_data(db)
        
        print("\n✓ Database seeding completed successfully!")
        print("\nYou can now test the API with the seeded data.")
        print("Example: GET http://localhost:8000/api/employees")
        
    except Exception as e:
        print(f"\n✗ Error during seeding: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()

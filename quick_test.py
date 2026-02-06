"""
Quick API Test Script

This script tests all API endpoints quickly to verify functionality.
"""

import requests
import json
from datetime import date

BASE_URL = "http://localhost:8000"


def test_health():
    """Test health endpoint."""
    print("\n1. Testing Health Check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")


def test_get_employees():
    """Test get all employees."""
    print("\n2. Testing GET /api/employees...")
    response = requests.get(f"{BASE_URL}/api/employees")
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Total Employees: {data.get('total', 0)}")
    if data.get('data'):
        print(f"   First Employee: {data['data'][0]['full_name']}")


def test_get_employee_by_id(employee_id=1):
    """Test get employee by ID."""
    print(f"\n3. Testing GET /api/employees/{employee_id}...")
    response = requests.get(f"{BASE_URL}/api/employees/{employee_id}")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Employee: {data['data']['full_name']}")


def test_create_employee():
    """Test create employee."""
    print("\n4. Testing POST /api/employees...")
    employee_data = {
        "employee_id": "EMP999",
        "full_name": "Test Employee",
        "email": "test.employee@company.com",
        "department": "Testing"
    }
    response = requests.post(
        f"{BASE_URL}/api/employees",
        json=employee_data
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 201:
        data = response.json()
        print(f"   Created: {data['data']['full_name']}")
        return data['data']['id']
    return None


def test_get_attendance():
    """Test get all attendance."""
    print("\n5. Testing GET /api/attendance...")
    response = requests.get(f"{BASE_URL}/api/attendance")
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Total Records: {data.get('total', 0)}")


def test_mark_attendance(employee_id=1):
    """Test mark attendance."""
    print(f"\n6. Testing POST /api/attendance...")
    attendance_data = {
        "employee_id": employee_id,
        "date": str(date.today()),
        "status": "Present"
    }
    response = requests.post(
        f"{BASE_URL}/api/attendance",
        json=attendance_data
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 201:
        data = response.json()
        print(f"   Marked attendance for: {data['data']['employee_name']}")


def test_employee_attendance(employee_id=1):
    """Test get employee attendance."""
    print(f"\n7. Testing GET /api/attendance/employee/{employee_id}...")
    response = requests.get(f"{BASE_URL}/api/attendance/employee/{employee_id}")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Records found: {data.get('total', 0)}")


def test_attendance_summary(employee_id=1):
    """Test get attendance summary."""
    print(f"\n8. Testing GET /api/attendance/summary/{employee_id}...")
    response = requests.get(f"{BASE_URL}/api/attendance/summary/{employee_id}")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()['data']
        print(f"   Employee: {data['employee_name']}")
        print(f"   Attendance: {data['attendance_percentage']}%")


def run_all_tests():
    """Run all tests."""
    print("="*60)
    print("HRMS LITE - API QUICK TEST")
    print("="*60)
    
    try:
        test_health()
        test_get_employees()
        test_get_employee_by_id(1)
        new_employee_id = test_create_employee()
        test_get_attendance()
        test_mark_attendance(1)
        test_employee_attendance(1)
        test_attendance_summary(1)
        
        print("\n" + "="*60)
        print("✓ All tests completed!")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Could not connect to API")
        print("   Make sure the server is running: python run.py")
    except Exception as e:
        print(f"\n✗ Error during testing: {str(e)}")


if __name__ == "__main__":
    run_all_tests()

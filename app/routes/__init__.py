"""
Routes Package

This package contains all API route handlers for the HRMS Lite application.
"""

from app.routes.employee import router as employee_router
from app.routes.attendance import router as attendance_router

__all__ = ["employee_router", "attendance_router"]

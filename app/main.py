"""
HRMS Lite API Main Application

This module initializes and configures the FastAPI application.
It sets up middleware, routes, exception handlers, and startup events.
"""

from contextlib import asynccontextmanager
from typing import Dict, Any
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.config import settings
from app.database import engine, Base
from app.routes.employee import router as employee_router
from app.routes.attendance import router as attendance_router
from app.utils.exceptions import HRMSException


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager.
    
    Handles startup and shutdown events.
    """
    # Startup: Log application start
    print(f"Starting {settings.app_title} v{settings.app_version}")
    print(f"Environment: {settings.environment}")
    print(f"CORS Origins: {settings.cors_origins_list}")
    
    yield
    
    # Shutdown: Cleanup resources
    print(f"Shutting down {settings.app_title}")


# Initialize FastAPI application
app = FastAPI(
    title=settings.app_title,
    version=settings.app_version,
    description=settings.app_description,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)


# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception Handlers
@app.exception_handler(HRMSException)
async def hrms_exception_handler(
    request: Request,
    exc: HRMSException
) -> JSONResponse:
    """
    Handle custom HRMS exceptions.
    
    Args:
        request: FastAPI request object
        exc: HRMS exception instance
        
    Returns:
        JSONResponse with error details
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict()
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
) -> JSONResponse:
    """
    Handle Pydantic validation errors.
    
    Args:
        request: FastAPI request object
        exc: Validation error instance
        
    Returns:
        JSONResponse with validation error details
    """
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        errors.append({
            "field": field,
            "message": error["msg"],
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": "Validation error",
            "status_code": 422,
            "details": errors
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(
    request: Request,
    exc: Exception
) -> JSONResponse:
    """
    Handle unexpected exceptions.
    
    Args:
        request: FastAPI request object
        exc: Exception instance
        
    Returns:
        JSONResponse with generic error message
    """
    # Log the error in production
    if settings.is_production:
        print(f"Unexpected error: {str(exc)}")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": "Internal server error",
            "status_code": 500,
            "details": {} if settings.is_production else {"message": str(exc)}
        }
    )


# Include API routers
app.include_router(employee_router)
app.include_router(attendance_router)


# Root endpoint
@app.get(
    "/",
    response_model=Dict[str, Any],
    tags=["Root"],
    summary="API Information",
    description="Get basic information about the HRMS Lite API."
)
async def root() -> Dict[str, Any]:
    """
    Root endpoint returning API information.
    
    Returns:
        Dict containing API metadata
    """
    return {
        "success": True,
        "data": {
            "name": settings.app_title,
            "version": settings.app_version,
            "description": settings.app_description,
            "docs": "/docs",
            "health": "/health"
        },
        "message": "Welcome to HRMS Lite API"
    }


# Health check endpoint
@app.get(
    "/health",
    response_model=Dict[str, Any],
    tags=["Health"],
    summary="Health Check",
    description="Check if the API is running and healthy."
)
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint for monitoring.
    
    Returns:
        Dict containing health status
    """
    return {
        "success": True,
        "data": {
            "status": "healthy",
            "environment": settings.environment,
            "version": settings.app_version
        },
        "message": "API is running"
    }

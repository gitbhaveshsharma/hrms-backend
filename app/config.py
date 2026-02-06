"""
Application Configuration Module

This module handles all configuration settings for the HRMS Lite API.
Configuration is loaded from environment variables.
"""

import os
from typing import List
from functools import lru_cache
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Attributes:
        database_url: PostgreSQL connection string for Neon database
        cors_origins: Comma-separated list of allowed CORS origins
        app_title: Title of the API application
        app_version: Version of the API
        app_description: Description of the API
        environment: Current environment (development/production)
    """
    
    # Database Configuration
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql://localhost/hrms_lite"
    )
    
    # CORS Configuration
    cors_origins: str = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:3000,http://localhost:5173"
    )
    
    # Application Settings
    app_title: str = os.getenv("APP_TITLE", "HRMS Lite API")
    app_version: str = os.getenv("APP_VERSION", "1.0.0")
    app_description: str = os.getenv(
        "APP_DESCRIPTION",
        "Human Resource Management System API"
    )
    
    # Environment
    environment: str = os.getenv("ENVIRONMENT", "development")
    
    # Port (for Railway deployment)
    port: int = int(os.getenv("PORT", "8000"))
    
    @property
    def cors_origins_list(self) -> List[str]:
        """
        Parse CORS origins from comma-separated string to list.
        
        Returns:
            List[str]: List of allowed CORS origins
        """
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    @property
    def is_production(self) -> bool:
        """
        Check if the application is running in production mode.
        
        Returns:
            bool: True if production, False otherwise
        """
        return self.environment.lower() == "production"
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Uses lru_cache to create a singleton pattern for settings.
    
    Returns:
        Settings: Application settings instance
    """
    return Settings()


# Global settings instance
settings = get_settings()

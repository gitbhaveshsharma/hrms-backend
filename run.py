"""
HRMS Lite API Server Runner

This script starts the uvicorn server for the HRMS Lite API.
Usage: python run.py
"""

import uvicorn
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()


def main() -> None:
    """Run the HRMS Lite API server."""
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    environment = os.getenv("ENVIRONMENT", "development")
    
    # Enable reload only in development
    reload_enabled = environment == "development"
    
    print(f"Starting HRMS Lite API server...")
    print(f"Environment: {environment}")
    print(f"Server running at: http://{host}:{port}")
    print(f"API Documentation: http://{host}:{port}/docs")
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload_enabled,
        log_level="info"
    )


if __name__ == "__main__":
    main()

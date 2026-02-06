"""
Database Configuration Module

This module handles database connection setup for PostgreSQL (Neon).
Includes SQLAlchemy engine, session management, and base model class.
"""

from typing import Generator
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy.pool import NullPool
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Create SQLAlchemy engine with optimized settings for Neon
# Using NullPool for Neon serverless to reduce connection overhead
engine = create_engine(
    settings.database_url,
    poolclass=NullPool,  # No pooling for serverless - faster connection
    connect_args={
        "connect_timeout": 5,  # Reduced timeout for faster failure
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5,
    },
    echo=False,  # Disable SQL logging for better performance
    execution_options={
        "isolation_level": "READ COMMITTED"  # Optimize transaction isolation
    }
)

# Add event listener to log slow queries
@event.listens_for(engine, "before_cursor_execute")
def receive_before_cursor_execute(conn, cursor, statement, params, context, executemany):
    conn.info.setdefault('query_start_time', [])
    conn.info['query_start_time'].append(context)

@event.listens_for(engine, "after_cursor_execute")
def receive_after_cursor_execute(conn, cursor, statement, params, context, executemany):
    # Log queries that take more than 500ms
    total_time = context._execution_time if hasattr(context, '_execution_time') else 0
    if total_time > 0.5:
        logger.warning(f"Slow query ({total_time:.2f}s): {statement[:100]}...")

# Session factory for creating database sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all SQLAlchemy models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function that provides a database session.
    
    Creates a new database session for each request and ensures
    it is properly closed after the request is complete.
    
    Yields:
        Session: SQLAlchemy database session
        
    Example:
        @app.get("/items")
        def get_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()  # Commit if no exceptions
    except Exception:
        db.rollback()  # Rollback on error
        raise
    finally:
        db.close()


def init_db() -> None:
    """
    Initialize database tables.
    
    Creates all tables defined in the models.
    Note: In production, use Alembic migrations instead.
    """
    Base.metadata.create_all(bind=engine)


def test_connection() -> bool:
    """
    Test database connection.
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False

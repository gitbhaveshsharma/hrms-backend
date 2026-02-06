# HRMS Lite - Architecture Documentation

This document provides a comprehensive overview of the HRMS Lite backend architecture, design decisions, and implementation details.

## 📋 Table of Contents

- [System Overview](#system-overview)
- [Architecture Layers](#architecture-layers)
- [Design Patterns](#design-patterns)
- [Database Schema](#database-schema)
- [API Design](#api-design)
- [Error Handling Strategy](#error-handling-strategy)
- [Security Considerations](#security-considerations)
- [Performance Optimizations](#performance-optimizations)
- [Scalability Considerations](#scalability-considerations)
- [Development Workflow](#development-workflow)
- [Deployment Architecture](#deployment-architecture)
- [Code Organization](#code-organization)
- [Future Enhancements](#future-enhancements)

---

## System Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │ Web Browser │  │ Mobile App  │  │ Third-Party Services    │  │
│  └──────┬──────┘  └──────┬──────┘  └───────────┬─────────────┘  │
└─────────┴────────────────┴─────────────────────┴────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API GATEWAY LAYER                           │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              FastAPI Application                          │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌────────────────┐   │   │
│  │  │ CORS        │  │ Validation  │  │ Error Handling │   │   │
│  │  │ Middleware  │  │ (Pydantic)  │  │ Middleware     │   │   │
│  │  └─────────────┘  └─────────────┘  └────────────────┘   │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                            │
│  ┌─────────────────────┐        ┌─────────────────────┐         │
│  │   Employee Routes   │        │  Attendance Routes  │         │
│  │   /api/employees    │        │  /api/attendance    │         │
│  └──────────┬──────────┘        └──────────┬──────────┘         │
└─────────────┴───────────────────────────────┴───────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                   BUSINESS LOGIC LAYER                           │
│  ┌─────────────────────┐        ┌─────────────────────┐         │
│  │  Employee Service   │        │ Attendance Service  │         │
│  │  - CRUD operations  │        │ - Mark attendance   │         │
│  │  - Validation       │        │ - Statistics        │         │
│  │  - Business rules   │        │ - Reporting         │         │
│  └──────────┬──────────┘        └──────────┬──────────┘         │
└─────────────┴───────────────────────────────┴───────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DATA ACCESS LAYER                             │
│  ┌─────────────────────┐        ┌─────────────────────┐         │
│  │   Employee Model    │◄──────►│  Attendance Model   │         │
│  │   (SQLAlchemy)      │  1:N   │  (SQLAlchemy)       │         │
│  └──────────┬──────────┘        └──────────┬──────────┘         │
└─────────────┴───────────────────────────────┴───────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATABASE LAYER                              │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              PostgreSQL (Neon Serverless)                 │   │
│  │  ┌───────────────┐           ┌────────────────────┐      │   │
│  │  │   employees   │───────────│    attendance      │      │   │
│  │  │    table      │   FK      │      table         │      │   │
│  │  └───────────────┘           └────────────────────┘      │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### Component Relationships

```
┌─────────────────────────────────────────────────────────────┐
│                    Request Flow                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  HTTP Request                                                │
│       │                                                      │
│       ▼                                                      │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐  │
│  │ FastAPI │───►│ Routes  │───►│Services │───►│ Models  │  │
│  │  CORS   │    │ (API)   │    │ (Logic) │    │  (ORM)  │  │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘  │
│       │              │              │              │        │
│       │              │              │              ▼        │
│       │              │              │         ┌─────────┐  │
│       │              │              │         │   DB    │  │
│       │              │              │         └─────────┘  │
│       │              │              │              │        │
│       │              │              ◄──────────────┘        │
│       │              ◄──────────────┘                       │
│       ◄──────────────┘                                      │
│       │                                                      │
│       ▼                                                      │
│  HTTP Response                                               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Architecture Layers

### 1. Presentation Layer (Routes)

**Location:** `app/routes/`

**Responsibilities:**

- Handle HTTP requests and responses
- Route requests to appropriate service methods
- Format responses in consistent JSON structure
- Handle pagination parameters
- Apply response status codes

**Key Characteristics:**

- Thin controllers with minimal logic
- Delegates business logic to services
- Each route function is 20-30 lines max
- Uses dependency injection for database sessions

```python
# Example route structure
@router.post("", status_code=status.HTTP_201_CREATED)
def create_employee(
    employee: EmployeeCreate,      # Pydantic validation
    db: Session = Depends(get_db)  # Dependency injection
) -> Dict[str, Any]:
    created = EmployeeService.create_employee(db, employee)
    return {"success": True, "data": created, "message": "Created"}
```

### 2. Business Logic Layer (Services)

**Location:** `app/services/`

**Responsibilities:**

- Implement business rules and validation
- Orchestrate data access operations
- Handle complex transactions
- Raise appropriate exceptions
- Perform data transformations

**Key Characteristics:**

- Static methods for stateless operations
- Single responsibility per method
- Clear separation from data access
- Comprehensive error handling

```python
# Example service structure
class EmployeeService:
    @staticmethod
    def create_employee(db: Session, data: EmployeeCreate) -> Employee:
        # 1. Validate business rules
        if EmployeeService.get_employee_by_email(db, data.email):
            raise DuplicateEmployeeException(field="email")

        # 2. Create entity
        employee = Employee(**data.model_dump())

        # 3. Persist and return
        db.add(employee)
        db.commit()
        return employee
```

### 3. Data Access Layer (Models)

**Location:** `app/models/`

**Responsibilities:**

- Define database table schemas
- Manage entity relationships
- Provide ORM mappings
- Define table constraints and indexes

**Key Characteristics:**

- SQLAlchemy declarative models
- Type hints for all columns
- Relationship definitions
- Helper methods (to_dict, **repr**)

### 4. Database Layer

**Technology:** PostgreSQL (Neon Serverless)

**Configuration:** `app/database.py`

**Features:**

- Connection pooling (5 connections, 10 overflow)
- Connection health checks (pool_pre_ping)
- Automatic session management
- Transaction handling

---

## Design Patterns

### 1. Repository Pattern (Implicit)

Services act as repositories, encapsulating data access logic:

```python
# EmployeeService acts as repository
EmployeeService.get_employee_by_id(db, id)
EmployeeService.get_all_employees(db, skip, limit)
EmployeeService.create_employee(db, data)
```

### 2. Dependency Injection

FastAPI's dependency injection system is used for:

- Database session management
- Configuration injection
- Request validation

```python
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Usage in routes
@router.get("")
def get_employees(db: Session = Depends(get_db)):
    ...
```

### 3. Service Layer Pattern

Business logic is isolated in service classes:

```
Routes (HTTP) → Services (Business Logic) → Models (Data Access)
```

### 4. Factory Pattern

Used for creating database sessions and engines:

```python
# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Usage
db = SessionLocal()
```

### 5. Singleton Pattern (Configuration)

Settings are cached using lru_cache:

```python
@lru_cache()
def get_settings() -> Settings:
    return Settings()
```

---

## Database Schema

### Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        EMPLOYEES                             │
├─────────────────────────────────────────────────────────────┤
│ PK │ id            │ INTEGER       │ AUTO_INCREMENT         │
│    │ employee_id   │ VARCHAR(50)   │ UNIQUE, NOT NULL       │
│    │ full_name     │ VARCHAR(100)  │ NOT NULL               │
│    │ email         │ VARCHAR(255)  │ UNIQUE, NOT NULL       │
│    │ department    │ VARCHAR(100)  │ NOT NULL               │
│    │ created_at    │ TIMESTAMP     │ DEFAULT CURRENT_TIME   │
│    │ updated_at    │ TIMESTAMP     │ DEFAULT CURRENT_TIME   │
├─────────────────────────────────────────────────────────────┤
│ Indexes:                                                     │
│   - ix_employees_id (PRIMARY KEY)                           │
│   - ix_employees_employee_id (UNIQUE)                       │
│   - ix_employees_email (UNIQUE)                             │
│   - ix_employees_department                                  │
│   - ix_employees_full_name                                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ 1:N
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                       ATTENDANCE                             │
├─────────────────────────────────────────────────────────────┤
│ PK │ id            │ INTEGER       │ AUTO_INCREMENT         │
│ FK │ employee_id   │ INTEGER       │ REFERENCES employees   │
│    │ date          │ DATE          │ NOT NULL               │
│    │ status        │ VARCHAR(20)   │ CHECK (Present/Absent) │
│    │ created_at    │ TIMESTAMP     │ DEFAULT CURRENT_TIME   │
├─────────────────────────────────────────────────────────────┤
│ Constraints:                                                 │
│   - uq_employee_date (UNIQUE: employee_id, date)            │
│   - ck_attendance_status (CHECK: status IN ('Present',      │
│     'Absent'))                                               │
│   - FK employee_id → employees.id ON DELETE CASCADE         │
├─────────────────────────────────────────────────────────────┤
│ Indexes:                                                     │
│   - ix_attendance_id (PRIMARY KEY)                          │
│   - ix_attendance_employee_id                                │
│   - ix_attendance_date                                       │
│   - ix_attendance_employee_date (COMPOSITE)                  │
└─────────────────────────────────────────────────────────────┘
```

### Table Relationships

- **One-to-Many:** One Employee has Many Attendance records
- **Cascade Delete:** Deleting an employee removes all their attendance records
- **Unique Constraint:** One attendance record per employee per date

---

## API Design

### RESTful Principles

| Principle                 | Implementation                                  |
| ------------------------- | ----------------------------------------------- |
| **Stateless**             | Each request contains all necessary information |
| **Resource-based URLs**   | `/api/employees`, `/api/attendance`             |
| **HTTP Methods**          | GET (read), POST (create), DELETE (remove)      |
| **Standard Status Codes** | 200, 201, 400, 404, 409, 422, 500               |
| **JSON Responses**        | Consistent response format                      |

### Endpoint Naming Conventions

```
/api/{resource}           → Collection operations
/api/{resource}/{id}      → Single resource operations
/api/{resource}/{id}/{sub}→ Sub-resource operations
```

### Response Format Standards

**Success Response:**

```json
{
  "success": true,
  "data": { ... },
  "message": "Operation completed successfully"
}
```

**List Response:**

```json
{
  "success": true,
  "data": [ ... ],
  "total": 100,
  "message": "Records retrieved successfully"
}
```

**Error Response:**

```json
{
  "success": false,
  "error": "Description of the error",
  "status_code": 400,
  "details": { ... }
}
```

---

## Error Handling Strategy

### Exception Hierarchy

```
Exception (Python Built-in)
    │
    └── HRMSException (Base custom exception)
            │
            ├── EmployeeNotFoundException (404)
            │
            ├── DuplicateEmployeeException (409)
            │
            ├── DuplicateAttendanceException (409)
            │
            ├── InvalidDateException (400)
            │
            └── ValidationException (400)
```

### Error Propagation Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    Error Flow                                │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Service Layer (Business Error)                             │
│       │                                                      │
│       ▼                                                      │
│  Raise HRMSException                                         │
│       │                                                      │
│       ▼                                                      │
│  FastAPI Exception Handler                                   │
│       │                                                      │
│       ▼                                                      │
│  JSONResponse with proper status code                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### HTTP Status Codes

| Code | Meaning       | When Used                  |
| ---- | ------------- | -------------------------- |
| 200  | OK            | Successful GET, DELETE     |
| 201  | Created       | Successful POST            |
| 400  | Bad Request   | Validation errors          |
| 404  | Not Found     | Resource doesn't exist     |
| 409  | Conflict      | Duplicate entry            |
| 422  | Unprocessable | Pydantic validation failed |
| 500  | Server Error  | Unexpected errors          |

---

## Security Considerations

### Input Validation

```python
# Pydantic validation with regex
@field_validator("email")
def validate_email(cls, value: str) -> str:
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_pattern, value):
        raise ValueError("Invalid email format")
    return value.lower()
```

### SQL Injection Prevention

- SQLAlchemy ORM automatically parameterizes queries
- No raw SQL queries used
- All user input is validated before database operations

### CORS Configuration

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,  # Whitelist specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Environment Variables

- Sensitive data stored in `.env` file
- `.env` excluded from version control
- Production uses platform-specific secrets

---

## Performance Optimizations

### Database Indexing

```sql
-- Primary lookup optimization
CREATE INDEX ix_employees_employee_id ON employees(employee_id);
CREATE INDEX ix_employees_email ON employees(email);

-- Query optimization
CREATE INDEX ix_employees_department ON employees(department);
CREATE INDEX ix_attendance_date ON attendance(date);

-- Composite index for common queries
CREATE INDEX ix_attendance_employee_date ON attendance(employee_id, date);
```

### Connection Pooling

```python
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,   # Health check before use
    pool_size=5,          # Minimum connections
    max_overflow=10,      # Additional connections
    pool_recycle=300,     # Recycle after 5 minutes
)
```

### Query Optimization

- Lazy loading for relationships
- Pagination for list endpoints
- Efficient filtering at database level

---

## Scalability Considerations

### Stateless Design

- No server-side sessions
- Each request is independent
- Easy horizontal scaling

### Database Connection Management

- Connection pooling
- Automatic connection recycling
- Health checks

### Future Scaling Options

```
┌─────────────────────────────────────────────────────────────┐
│                    Scaling Architecture                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│        ┌────────────┐                                        │
│        │   Load     │                                        │
│        │  Balancer  │                                        │
│        └─────┬──────┘                                        │
│              │                                               │
│     ┌────────┼────────┐                                      │
│     ▼        ▼        ▼                                      │
│  ┌──────┐ ┌──────┐ ┌──────┐                                 │
│  │ API  │ │ API  │ │ API  │   (Horizontal Scaling)          │
│  │  #1  │ │  #2  │ │  #3  │                                 │
│  └──┬───┘ └──┬───┘ └──┬───┘                                 │
│     │        │        │                                      │
│     └────────┼────────┘                                      │
│              ▼                                               │
│        ┌────────────┐                                        │
│        │   Redis    │   (Future: Caching)                   │
│        │   Cache    │                                        │
│        └─────┬──────┘                                        │
│              │                                               │
│              ▼                                               │
│        ┌────────────┐                                        │
│        │ PostgreSQL │   (Read Replicas)                     │
│        │   (Neon)   │                                        │
│        └────────────┘                                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Development Workflow

### Local Setup

```bash
# 1. Clone and setup virtual environment
git clone <repo-url>
cd hrms-backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your settings

# 4. Run migrations
alembic upgrade head

# 5. Start development server
python run.py
```

### Migration Process

```bash
# Create new migration
alembic revision -m "description of changes"

# Auto-generate migration from model changes
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View history
alembic history
```

### Testing Approach

1. **Manual Testing:** Use Swagger UI at `/docs`
2. **API Testing:** Use Postman or cURL
3. **Database Testing:** Verify data in Neon dashboard

---

## Deployment Architecture

### Production Environment

```
┌─────────────────────────────────────────────────────────────┐
│                  Production Deployment                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Render / Railway                         │   │
│  │  ┌────────────────────────────────────────────────┐  │   │
│  │  │              HRMS Lite API                      │  │   │
│  │  │         (FastAPI + Uvicorn)                     │  │   │
│  │  │                                                 │  │   │
│  │  │  Environment Variables:                         │  │   │
│  │  │  - DATABASE_URL                                 │  │   │
│  │  │  - CORS_ORIGINS                                 │  │   │
│  │  │  - ENVIRONMENT=production                       │  │   │
│  │  └────────────────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────┘   │
│                           │                                  │
│                           │ HTTPS                            │
│                           ▼                                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                  Neon PostgreSQL                      │   │
│  │              (Serverless Database)                    │   │
│  │                                                       │   │
│  │  - Auto-scaling                                       │   │
│  │  - Automatic backups                                  │   │
│  │  - SSL encryption                                     │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Environment Variables

| Variable     | Description                  | Example            |
| ------------ | ---------------------------- | ------------------ |
| DATABASE_URL | PostgreSQL connection string | `postgresql://...` |
| CORS_ORIGINS | Allowed frontend URLs        | `https://app.com`  |
| ENVIRONMENT  | Runtime environment          | `production`       |
| APP_TITLE    | API title                    | `HRMS Lite API`    |
| APP_VERSION  | API version                  | `1.0.0`            |

---

## Code Organization Principles

### Separation of Concerns

```
Routes      → HTTP handling, request/response formatting
Services    → Business logic, validation, orchestration
Models      → Data structure, database schema
Schemas     → Input/output validation
Utils       → Shared utilities, exceptions
```

### Single Responsibility

Each module has one clear purpose:

- `employee.py` (routes) → Employee HTTP endpoints
- `employee_service.py` → Employee business logic
- `employee.py` (models) → Employee data structure
- `employee.py` (schemas) → Employee validation

### DRY Principle

- Reusable validators in `utils/validators.py`
- Common exception classes in `utils/exceptions.py`
- Shared database session in `database.py`

### Code Quality Standards

- **Function Size:** 20-30 lines maximum
- **Type Hints:** All functions and parameters
- **Docstrings:** All public functions
- **Naming:** Descriptive snake_case

---

## Future Enhancements

### Phase 1: Security

- [ ] JWT Authentication
- [ ] Role-based access control
- [ ] API rate limiting
- [ ] Request logging

### Phase 2: Features

- [ ] Leave management
- [ ] Department CRUD
- [ ] Bulk operations
- [ ] Report generation

### Phase 3: Performance

- [ ] Redis caching
- [ ] Query optimization
- [ ] Database read replicas
- [ ] CDN integration

### Phase 4: DevOps

- [ ] Unit tests (pytest)
- [ ] Integration tests
- [ ] CI/CD pipeline
- [ ] Docker containerization

---

## Conclusion

HRMS Lite is built with a focus on:

1. **Clean Architecture:** Clear separation of concerns
2. **Maintainability:** Easy to understand and extend
3. **Scalability:** Ready for growth
4. **Production-Ready:** Proper error handling and logging

This architecture ensures that the application can evolve with changing requirements while maintaining code quality and performance.

---

_Last Updated: January 2024_
_Version: 1.0.0_

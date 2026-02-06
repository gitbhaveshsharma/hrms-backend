# HRMS Lite API

A production-ready REST API backend for a Human Resource Management System (HRMS) built with Python FastAPI, PostgreSQL (Neon), SQLAlchemy, and Alembic.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Table of Contents

- [Tech Stack](#-tech-stack)
- [Features](#-features)
- [Folder Structure](#-folder-structure)
- [Prerequisites](#-prerequisites)
- [Environment Setup](#-environment-setup)
- [Database Setup](#-database-setup)
- [Running Locally](#-running-locally)
- [API Endpoints](#-api-endpoints)
- [API Documentation](#-api-documentation)
- [Deployment](#-deployment)
- [Testing](#-testing)
- [Project Assumptions](#-project-assumptions)
- [Future Improvements](#-future-improvements)
- [Author](#-author)

## 🛠 Tech Stack

| Technology    | Version | Purpose                    |
| ------------- | ------- | -------------------------- |
| Python        | 3.11+   | Programming Language       |
| FastAPI       | 0.109.0 | Web Framework              |
| PostgreSQL    | Latest  | Database (Neon Serverless) |
| SQLAlchemy    | 2.0.25  | ORM                        |
| Alembic       | 1.13.1  | Database Migrations        |
| Pydantic      | 2.5.3   | Data Validation            |
| Uvicorn       | 0.27.0  | ASGI Server                |
| python-dotenv | 1.0.0   | Environment Variables      |

## ✨ Features

### Employee Management

- ✅ Create new employees with unique ID and email
- ✅ Retrieve all employees with pagination
- ✅ Get employee by ID
- ✅ Delete employee (cascades to attendance records)
- ✅ Search employees by department

### Attendance Management

- ✅ Mark attendance (Present/Absent) for employees
- ✅ Retrieve all attendance records
- ✅ Filter attendance by date
- ✅ Get attendance history for specific employee
- ✅ Calculate attendance statistics/summary

### Additional Features

- ✅ Professional error handling with custom exceptions
- ✅ Input validation with Pydantic v2
- ✅ CORS configuration for frontend integration
- ✅ Health check endpoint for monitoring
- ✅ Interactive API documentation (Swagger UI)
- ✅ Database migrations with Alembic

## 📁 Folder Structure

```
hrms-backend/
├── alembic/
│   ├── versions/
│   │   ├── 001_create_employees_table.py
│   │   └── 002_create_attendance_table.py
│   ├── env.py
│   └── script.py.mako
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app initialization
│   ├── database.py          # Database connection setup
│   ├── config.py            # Configuration settings
│   ├── models/
│   │   ├── __init__.py
│   │   ├── employee.py      # Employee SQLAlchemy model
│   │   └── attendance.py    # Attendance SQLAlchemy model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── employee.py      # Employee Pydantic schemas
│   │   └── attendance.py    # Attendance Pydantic schemas
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── employee.py      # Employee API endpoints
│   │   └── attendance.py    # Attendance API endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── employee_service.py    # Employee business logic
│   │   └── attendance_service.py  # Attendance business logic
│   └── utils/
│       ├── __init__.py
│       ├── validators.py    # Validation utilities
│       └── exceptions.py    # Custom exceptions
├── .env                     # Environment variables (not in git)
├── .env.example             # Example environment file
├── .gitignore
├── alembic.ini              # Alembic configuration
├── requirements.txt
├── run.py                   # Server startup script
├── README.md
└── ARCHITECTURE.md
```

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11+** - [Download Python](https://www.python.org/downloads/)
- **pip** - Python package manager (included with Python)
- **Git** - Version control system
- **PostgreSQL** - Or use Neon serverless PostgreSQL

## 🔧 Environment Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd hrms-backend
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables

Create a `.env` file in the project root:

```bash
# Copy from example
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@host/database?sslmode=require

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Application Settings
APP_TITLE=HRMS Lite API
APP_VERSION=1.0.0
APP_DESCRIPTION=Human Resource Management System API

# Environment
ENVIRONMENT=development
```

## 🗄 Database Setup

### Using Neon PostgreSQL (Recommended)

1. **Create Neon Account**: Go to [neon.tech](https://neon.tech) and sign up
2. **Create New Project**: Click "New Project" and name it "hrms-lite"
3. **Copy Connection String**: Go to Dashboard > Connection Details
4. **Update .env**: Paste the connection string as `DATABASE_URL`

```env
DATABASE_URL=postgresql://username:password@ep-xxx.us-east-2.aws.neon.tech/hrms_lite?sslmode=require
```

### Run Migrations

```bash
# Run all migrations
alembic upgrade head

# Check current migration status
alembic current

# View migration history
alembic history
```

## 🚀 Running Locally

### Option 1: Using run.py

```bash
python run.py
```

### Option 2: Using uvicorn directly

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Access the API

- **API Base URL**: http://localhost:8000
- **Swagger Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📡 API Endpoints

### Root & Health

| Method | Endpoint  | Description     |
| ------ | --------- | --------------- |
| GET    | `/`       | API information |
| GET    | `/health` | Health check    |

### Employees

| Method | Endpoint              | Description         |
| ------ | --------------------- | ------------------- |
| POST   | `/api/employees`      | Create new employee |
| GET    | `/api/employees`      | Get all employees   |
| GET    | `/api/employees/{id}` | Get employee by ID  |
| DELETE | `/api/employees/{id}` | Delete employee     |

### Attendance

| Method | Endpoint                          | Description                |
| ------ | --------------------------------- | -------------------------- |
| POST   | `/api/attendance`                 | Mark attendance            |
| GET    | `/api/attendance`                 | Get all attendance records |
| GET    | `/api/attendance?date=YYYY-MM-DD` | Filter by date             |
| GET    | `/api/attendance/employee/{id}`   | Get employee attendance    |
| GET    | `/api/attendance/summary/{id}`    | Get attendance summary     |

### Example Requests & Responses

#### Create Employee

**Request:**

```bash
POST /api/employees
Content-Type: application/json

{
  "employee_id": "EMP001",
  "full_name": "John Doe",
  "email": "john.doe@company.com",
  "department": "Engineering"
}
```

**Response:**

```json
{
  "success": true,
  "data": {
    "id": 1,
    "employee_id": "EMP001",
    "full_name": "John Doe",
    "email": "john.doe@company.com",
    "department": "Engineering",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  },
  "message": "Employee created successfully"
}
```

#### Mark Attendance

**Request:**

```bash
POST /api/attendance
Content-Type: application/json

{
  "employee_id": 1,
  "date": "2024-01-15",
  "status": "Present"
}
```

**Response:**

```json
{
  "success": true,
  "data": {
    "id": 1,
    "employee_id": 1,
    "date": "2024-01-15",
    "status": "Present",
    "created_at": "2024-01-15T10:35:00",
    "employee_name": "John Doe",
    "employee_code": "EMP001"
  },
  "message": "Attendance marked successfully"
}
```

## 📖 API Documentation

FastAPI provides interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
  - Interactive testing interface
  - Try out endpoints directly
  - View request/response schemas

- **ReDoc**: http://localhost:8000/redoc
  - Clean, readable documentation
  - Detailed schema information

## 🌐 Deployment

### Deploy to Render

1. **Create Render Account**: Go to [render.com](https://render.com)

2. **Create New Web Service**:
   - Connect your GitHub repository
   - Select the `hrms-backend` repository

3. **Configure Service**:
   - **Name**: hrms-lite-api
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Set Environment Variables**:

   ```
   DATABASE_URL=<your-neon-connection-string>
   CORS_ORIGINS=https://your-frontend-url.com
   ENVIRONMENT=production
   ```

5. **Deploy**: Click "Create Web Service"

### Deploy to Railway

1. **Create Railway Account**: Go to [railway.app](https://railway.app)

2. **New Project**: Click "New Project" > "Deploy from GitHub"

3. **Select Repository**: Choose your `hrms-backend` repo

4. **Add Variables**:
   - Go to Variables tab
   - Add all environment variables from `.env.example`

5. **Deploy**: Railway will auto-deploy

### Post-Deployment

1. Update `CORS_ORIGINS` with your deployed frontend URL
2. Run migrations: Connect via Railway/Render shell and run `alembic upgrade head`
3. Test API at `https://your-api-url.com/docs`

## 🧪 Testing

### Manual Testing with Swagger UI

1. Open http://localhost:8000/docs
2. Click on an endpoint
3. Click "Try it out"
4. Fill in the request body
5. Click "Execute"

### Testing with cURL

```bash
# Health check
curl http://localhost:8000/health

# Create employee
curl -X POST http://localhost:8000/api/employees \
  -H "Content-Type: application/json" \
  -d '{"employee_id":"EMP001","full_name":"John Doe","email":"john@example.com","department":"Engineering"}'

# Get all employees
curl http://localhost:8000/api/employees

# Mark attendance
curl -X POST http://localhost:8000/api/attendance \
  -H "Content-Type: application/json" \
  -d '{"employee_id":1,"date":"2024-01-15","status":"Present"}'
```

### Testing Checklist

- [ ] All migrations run successfully
- [ ] All endpoints return correct responses
- [ ] Validation errors show proper messages
- [ ] Duplicate entries are prevented
- [ ] Foreign key constraints work
- [ ] CORS allows frontend origin
- [ ] API documentation works at /docs
- [ ] Environment variables load correctly
- [ ] Database connection is stable
- [ ] Error handling covers all cases

## 📝 Project Assumptions

1. **Single Attendance Per Day**: An employee can only have one attendance record per day
2. **No Future Dates**: Attendance cannot be marked for future dates
3. **Status Values**: Only "Present" and "Absent" are valid status values
4. **Email Format**: Standard email validation is enforced
5. **Cascade Delete**: Deleting an employee removes all their attendance records
6. **No Authentication**: This version doesn't include user authentication (future enhancement)

## 🔮 Future Improvements

### High Priority

- [ ] User authentication and authorization (JWT)
- [ ] Password-protected admin panel
- [ ] Bulk attendance marking
- [ ] Export attendance reports (CSV/PDF)

### Medium Priority

- [ ] Leave management module
- [ ] Employee profile pictures
- [ ] Department management CRUD
- [ ] Email notifications

### Low Priority

- [ ] API rate limiting
- [ ] Redis caching layer
- [ ] API versioning (v1, v2)
- [ ] WebSocket for real-time updates
- [ ] Comprehensive unit and integration tests

## 👤 Author

**HRMS Lite Team**

- GitHub: [@your-username](https://github.com/your-username)
- Email: your.email@example.com

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Made with ❤️ using FastAPI and Python

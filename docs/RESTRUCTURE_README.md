# FastAPI Modular Structure

This document describes the restructured FastAPI application following Django-style modular organization.

## 📁 Directory Structure

```
fastapi-learn/
├── app/                          # Main application package
│   ├── __init__.py              # Package initialization
│   └── core/                    # Core application modules
│       ├── __init__.py          # Package initialization
│       ├── main.py              # FastAPI application and routes
│       ├── models.py            # SQLAlchemy database models
│       └── database.py          # Database configuration and session management
├── docker/                      # Docker-related configurations
│   └── compose/                 # Docker Compose files
│       └── docker-compose.yml   # PostgreSQL service definition
├── migrations/                  # Alembic database migrations
│   ├── env.py                   # Alembic environment configuration
│   ├── script.py.mako          # Migration template
│   └── versions/               # Migration files
├── docs/                       # Documentation files
├── schemas.py                  # Pydantic schemas (kept at root for now)
├── main.py                     # Application entry point
├── alembic.ini                 # Alembic configuration
├── migrate.py                  # Migration helper script
├── pyproject.toml              # Project dependencies
├── README.md                   # This file
├── SECURITY_GUIDE.md           # Security documentation
└── .env                        # Environment variables (not in repo)
```

## 🚀 Running the Application

### Using the Entry Point
```bash
python main.py
```

### Using Uvicorn directly
```bash
uvicorn app.core.main:app --reload
```

## 🐳 Docker Usage

### Start PostgreSQL
```bash
docker-compose -f docker/compose/docker-compose.yml up -d postgres
```

### Stop Services
```bash
docker-compose -f docker/compose/docker-compose.yml down
```

## 🗄️ Database Migrations

All Alembic commands work as before from the project root:

```bash
# Check current migration status
python -m alembic current

# Create new migration
python -m alembic revision --autogenerate -m "description"

# Apply migrations
python -m alembic upgrade head

# Rollback migration
python -m alembic downgrade -1
```

Or use the helper script:
```bash
python migrate.py current
python migrate.py create "description"
python migrate.py upgrade head
```

## 📦 Import Structure

### Within the app package
```python
# Relative imports within core
from .models import Base, Product
from .database import get_session
```

### From external modules
```python
# Absolute imports from outside the app
from app.core.main import app
from app.core.models import Product
from app.core.database import get_session
```

## 🧪 Testing the Structure

Run the included test script to verify everything works:
```bash
python test_restructure.py
```

## 📝 Key Changes Made

1. **Created modular structure**: `app/core/` contains main application logic
2. **Moved Docker files**: `docker/compose/` contains Docker configurations  
3. **Updated imports**: All relative imports updated to work with new structure
4. **Maintained compatibility**: Alembic, Docker Compose, and application entry points all work as before
5. **Added entry point**: New `main.py` at root imports from modular structure

## 🔄 Migration Notes

- **Alembic**: Updated `migrations/env.py` to import from `app.core.models` and `app.core.database`
- **Docker**: Moved to `docker/compose/docker-compose.yml` - use `-f` flag when running
- **Entry Point**: New `main.py` at root provides backward compatibility
- **Dependencies**: No changes to `pyproject.toml` or requirements

## 🎯 Future Modularization

This basic restructuring provides foundation for further modularization:

- `app/auth/` - Authentication and authorization
- `app/api/` - API route handlers
- `app/services/` - Business logic services
- `app/utils/` - Utility functions
- `app/config/` - Configuration management

## ⚠️ Important Notes

- Always run commands from the project root directory
- Use `-f docker/compose/docker-compose.yml` when using Docker Compose
- Environment variables (`.env`) location remains at project root
- Schemas remain at root level for now - can be moved later if needed
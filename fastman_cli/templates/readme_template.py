"""README template generator."""

from datetime import datetime


def generate_readme(module_name: str, class_name: str) -> str:
    """Generate README.md file for module."""
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    return f'''# {class_name} Module

**Generated on:** {current_date}

## Overview

The {class_name} module provides a complete CRUD implementation for managing {module_name}s in the FastAPI application.

## Structure

```
{module_name}/
├── __init__.py         # Module exports
├── models.py          # SQLAlchemy models
├── schemas.py         # Pydantic schemas
├── crud.py            # CRUD operations
├── services.py        # Business logic
├── routes.py          # API endpoints
├── exceptions.py      # Custom exceptions
└── README.md          # This file
```

## Components

### Models (`models.py`)
SQLAlchemy model defining the database table structure for {module_name}s.

**Fields:**
- `id`: Primary key
- `name`: {class_name} name (required, indexed)
- `description`: Optional description
- `is_active`: Active status (default: True)
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Schemas (`schemas.py`)
Pydantic schemas for request/response validation:
- `{class_name}Base`: Base schema with common fields
- `{class_name}Create`: Schema for creating {module_name}s
- `{class_name}Update`: Schema for updating {module_name}s
- `{class_name}`: Response schema with all fields
- `{class_name}InDB`: Database representation

### CRUD (`crud.py`)
Database operations extending `CRUDBase`:
- `get()`: Get {module_name} by ID
- `get_multi()`: Get multiple {module_name}s with pagination
- `get_by_name()`: Get {module_name} by name
- `get_active()`: Get active {module_name}s only
- `create()`: Create new {module_name}
- `update()`: Update existing {module_name}
- `deactivate()`: Soft delete (set is_active=False)
- `remove()`: Hard delete from database

### Services (`services.py`)
Business logic layer:
- `get_all_{module_name}s()`: Get all {module_name}s with filtering
- `get_{module_name}_by_id()`: Get specific {module_name}
- `create_{module_name}()`: Create with validation
- `update_{module_name}()`: Update with validation
- `delete_{module_name}()`: Delete (soft/hard)
- `get_{module_name}_by_name()`: Get by name

### Routes (`routes.py`)
FastAPI endpoints:
- `GET /{module_name}s/`: List all {module_name}s
- `GET /{module_name}s/{{id}}`: Get specific {module_name}
- `POST /{module_name}s/`: Create new {module_name}
- `PUT /{module_name}s/{{id}}`: Update {module_name}
- `DELETE /{module_name}s/{{id}}`: Delete {module_name}
- `GET /{module_name}s/name/{{name}}`: Get by name

### Exceptions (`exceptions.py`)
Custom exceptions:
- `{class_name}Exception`: Base exception
- `{class_name}NotFoundError`: {class_name} not found
- `{class_name}AlreadyExistsError`: Duplicate name
- `Invalid{class_name}DataError`: Invalid data

## Usage

### Import the module
```python
from app.{module_name} import router, {class_name}Service
```

### Register routes
```python
# In app/apis/v1.py
from app.{module_name}.routes import router as {module_name}_router

router = APIRouter(prefix="/v1")
router.include_router({module_name}_router)
```

### Use in code
```python
from sqlalchemy.ext.asyncio import AsyncSession
from app.{module_name}.services import {class_name}Service
from app.{module_name}.schemas import {class_name}Create

# Create a {module_name}
{module_name}_data = {class_name}Create(
    name="Example {class_name}",
    description="This is an example"
)
{module_name} = await {class_name}Service.create_{module_name}(session, {module_name}_data)
```

## Database Migration

After creating this module, generate and run migrations:

```bash
# Generate migration
alembic revision --autogenerate -m "Add {module_name} table"

# Run migration
alembic upgrade head
```

## Testing

Create tests in `tests/test_{module_name}.py`:

```python
import pytest
from app.{module_name}.schemas import {class_name}Create

@pytest.mark.asyncio
async def test_create_{module_name}(session):
    # Your test code here
    pass
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Look for the "{class_name}s" tag to see all endpoints.

## Next Steps

1. **Add to API Router**: Include this module's router in `app/apis/v1.py`
2. **Generate Migration**: Create database migration with Alembic
3. **Add Tests**: Create comprehensive tests
4. **Customize**: Modify models and business logic as needed
5. **Add Relationships**: Link to other models if required

## Notes

- This module follows the modular architecture pattern
- All operations are asynchronous
- Soft delete is enabled by default
- Logging is configured for all operations
- Exception handling is standardized
'''

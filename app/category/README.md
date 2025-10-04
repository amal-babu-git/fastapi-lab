# Category Module

**Generated on:** 2025-10-04

## Overview

The Category module provides a complete CRUD implementation for managing categorys in the FastAPI application.

## Structure

```
category/
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
SQLAlchemy model defining the database table structure for categorys.

**Fields:**
- `id`: Primary key
- `name`: Category name (required, indexed)
- `description`: Optional description
- `is_active`: Active status (default: True)
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Schemas (`schemas.py`)
Pydantic schemas for request/response validation:
- `CategoryBase`: Base schema with common fields
- `CategoryCreate`: Schema for creating categorys
- `CategoryUpdate`: Schema for updating categorys
- `Category`: Response schema with all fields
- `CategoryInDB`: Database representation

### CRUD (`crud.py`)
Database operations extending `CRUDBase`:
- `get()`: Get category by ID
- `get_multi()`: Get multiple categorys with pagination
- `get_by_name()`: Get category by name
- `get_active()`: Get active categorys only
- `create()`: Create new category
- `update()`: Update existing category
- `deactivate()`: Soft delete (set is_active=False)
- `remove()`: Hard delete from database

### Services (`services.py`)
Business logic layer:
- `get_all_categorys()`: Get all categorys with filtering
- `get_category_by_id()`: Get specific category
- `create_category()`: Create with validation
- `update_category()`: Update with validation
- `delete_category()`: Delete (soft/hard)
- `get_category_by_name()`: Get by name

### Routes (`routes.py`)
FastAPI endpoints:
- `GET /categorys/`: List all categorys
- `GET /categorys/{id}`: Get specific category
- `POST /categorys/`: Create new category
- `PUT /categorys/{id}`: Update category
- `DELETE /categorys/{id}`: Delete category
- `GET /categorys/name/{name}`: Get by name

### Exceptions (`exceptions.py`)
Custom exceptions:
- `CategoryException`: Base exception
- `CategoryNotFoundError`: Category not found
- `CategoryAlreadyExistsError`: Duplicate name
- `InvalidCategoryDataError`: Invalid data

## Usage

### Import the module
```python
from app.category import router, CategoryService
```

### Register routes
```python
# In app/apis/v1.py
from app.category.routes import router as category_router

router = APIRouter(prefix="/v1")
router.include_router(category_router)
```

### Use in code
```python
from sqlalchemy.ext.asyncio import AsyncSession
from app.category.services import CategoryService
from app.category.schemas import CategoryCreate

# Create a category
category_data = CategoryCreate(
    name="Example Category",
    description="This is an example"
)
category = await CategoryService.create_category(session, category_data)
```

## Database Migration

After creating this module, generate and run migrations:

```bash
# Generate migration
alembic revision --autogenerate -m "Add category table"

# Run migration
alembic upgrade head
```

## Testing

Create tests in `tests/test_category.py`:

```python
import pytest
from app.category.schemas import CategoryCreate

@pytest.mark.asyncio
async def test_create_category(session):
    # Your test code here
    pass
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Look for the "Categorys" tag to see all endpoints.

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

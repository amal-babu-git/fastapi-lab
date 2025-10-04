# Module Structure Reference Guide

## Quick Reference for Creating New Modules

Use this as a template when creating new modules (e.g., `user`, `order`, `category`).

---

## Step-by-Step Guide

### 1. Create Module Directory

```bash
mkdir app/{module_name}
cd app/{module_name}
```

### 2. Create Files

Create these files in order:

```
app/{module_name}/
├── __init__.py
├── models.py
├── schemas.py
├── crud.py
├── exceptions.py
├── services.py
├── routes.py
└── README.md
```

---

## File Templates

### `models.py` - Database Schema

```python
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Float, Boolean, DateTime
from app.core.database import Base


class YourModel(Base):
    """Model for {description}."""

    __tablename__ = "your_table"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    # Add your fields here
```

---

### `schemas.py` - Pydantic Models

```python
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class YourModelBase(BaseModel):
    """Base schema with common fields."""
    name: str = Field(..., min_length=1, max_length=255)
    # Add your fields here


class YourModelCreate(YourModelBase):
    """Schema for creating new records."""
    pass


class YourModelUpdate(BaseModel):
    """Schema for updating records (partial updates)."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    # Add optional fields here


class YourModel(YourModelBase):
    """Schema for responses (includes ID)."""
    id: int
    
    model_config = ConfigDict(from_attributes=True)
```

---

### `crud.py` - Data Access Layer

```python
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.crud import CRUDBase
from .models import YourModel
from .schemas import YourModelCreate, YourModelUpdate


class YourModelCRUD(CRUDBase[YourModel, YourModelCreate, YourModelUpdate]):
    """CRUD operations for YourModel."""

    def __init__(self):
        super().__init__(YourModel)

    # Add custom query methods here
    async def get_by_name(
        self, 
        session: AsyncSession, 
        name: str
    ) -> Optional[YourModel]:
        """Get a record by name."""
        result = await session.execute(
            select(YourModel).where(YourModel.name == name)
        )
        return result.scalar_one_or_none()


# Create a singleton instance
your_model_crud = YourModelCRUD()
```

---

### `exceptions.py` - Custom Exceptions

```python
"""Custom exceptions for the {module_name} module."""


class YourModelException(Exception):
    """Base exception for all {module_name}-related errors."""
    pass


class YourModelNotFoundError(YourModelException):
    """Raised when a record is not found."""
    
    def __init__(self, id: int):
        self.id = id
        super().__init__(f"YourModel with ID {id} not found")


class YourModelAlreadyExistsError(YourModelException):
    """Raised when attempting to create a duplicate record."""
    
    def __init__(self, name: str):
        self.name = name
        super().__init__(f"YourModel with name '{name}' already exists")


# Add more custom exceptions as needed
```

---

### `services.py` - Business Logic Layer

```python
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from .models import YourModel
from .schemas import YourModelCreate, YourModelUpdate
from .crud import your_model_crud
from .exceptions import (
    YourModelNotFoundError,
    YourModelAlreadyExistsError,
)


class YourModelService:
    """Service layer for {module_name} business logic."""

    @staticmethod
    async def get_all(
        session: AsyncSession, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[YourModel]:
        """Get all records with pagination."""
        return await your_model_crud.get_multi(session, skip=skip, limit=limit)

    @staticmethod
    async def get_by_id(
        session: AsyncSession, 
        id: int
    ) -> Optional[YourModel]:
        """Get a record by ID."""
        return await your_model_crud.get(session, id)

    @staticmethod
    async def create(
        session: AsyncSession, 
        data: YourModelCreate
    ) -> YourModel:
        """Create a new record with validation."""
        # Business validation
        existing = await your_model_crud.get_by_name(session, data.name)
        if existing:
            raise YourModelAlreadyExistsError(data.name)
        
        # Add more business logic here
        
        return await your_model_crud.create(session, obj_in=data)

    @staticmethod
    async def update(
        session: AsyncSession, 
        id: int, 
        data: YourModelUpdate
    ) -> YourModel:
        """Update an existing record with validation."""
        # Check if exists
        record = await your_model_crud.get(session, id)
        if not record:
            raise YourModelNotFoundError(id)
        
        # Business validation
        if data.name:
            existing = await your_model_crud.get_by_name(session, data.name)
            if existing and existing.id != id:
                raise YourModelAlreadyExistsError(data.name)
        
        return await your_model_crud.update(session, db_obj=record, obj_in=data)

    @staticmethod
    async def delete(session: AsyncSession, id: int) -> bool:
        """Delete a record."""
        record = await your_model_crud.get(session, id)
        if not record:
            raise YourModelNotFoundError(id)
        
        return await your_model_crud.remove(session, id=id)
```

---

### `routes.py` - API Endpoints

```python
from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_session
from .schemas import YourModel, YourModelCreate, YourModelUpdate
from .services import YourModelService
from .exceptions import (
    YourModelNotFoundError,
    YourModelAlreadyExistsError,
)

router = APIRouter(prefix="/your-route", tags=["your_tag"])


@router.get("/", response_model=List[YourModel])
async def get_all(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    session: AsyncSession = Depends(get_session)
):
    """Get all records with pagination."""
    records = await YourModelService.get_all(session, skip, limit)
    return records


@router.get("/{id}", response_model=YourModel)
async def get_by_id(id: int, session: AsyncSession = Depends(get_session)):
    """Get a record by ID."""
    record = await YourModelService.get_by_id(session, id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Record with ID {id} not found"
        )
    return record


@router.post("/", response_model=YourModel, status_code=status.HTTP_201_CREATED)
async def create(
    data: YourModelCreate, 
    session: AsyncSession = Depends(get_session)
):
    """Create a new record."""
    try:
        record = await YourModelService.create(session, data)
        return record
    except YourModelAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create record: {str(e)}"
        )


@router.put("/{id}", response_model=YourModel)
async def update(
    id: int,
    data: YourModelUpdate,
    session: AsyncSession = Depends(get_session)
):
    """Update an existing record."""
    try:
        record = await YourModelService.update(session, id, data)
        return record
    except YourModelNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except YourModelAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update record: {str(e)}"
        )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int, session: AsyncSession = Depends(get_session)):
    """Delete a record."""
    try:
        await YourModelService.delete(session, id)
    except YourModelNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete record: {str(e)}"
        )
```

---

### `__init__.py` - Module Exports

```python
"""
{Module Name} module for managing {description}.

This module provides a complete CRUD implementation.
"""

from .models import YourModel
from .schemas import (
    YourModelBase, 
    YourModelCreate, 
    YourModelUpdate, 
    YourModel as YourModelSchema
)
from .routes import router
from .services import YourModelService
from .crud import your_model_crud
from .exceptions import (
    YourModelException,
    YourModelNotFoundError,
    YourModelAlreadyExistsError,
)

__all__ = [
    "YourModel",
    "YourModelBase",
    "YourModelCreate",
    "YourModelUpdate",
    "YourModelSchema",
    "router",
    "YourModelService",
    "your_model_crud",
    "YourModelException",
    "YourModelNotFoundError",
    "YourModelAlreadyExistsError",
]
```

---

## Integration Steps

### 1. Register Router in Main App

In `app/core/main.py`:

```python
from app.your_module.routes import router as your_module_router

app.include_router(your_module_router)
```

### 2. Create Database Migration

```bash
# Using Alembic
alembic revision --autogenerate -m "Add your_model table"
alembic upgrade head
```

### 3. Test the API

```bash
# Start server
uvicorn app.core.main:app --reload

# Test endpoints
curl http://localhost:8000/your-route/
```

---

## Checklist

When creating a new module, ensure:

- [ ] Models defined with proper types
- [ ] Schemas for Create, Update, and Response
- [ ] CRUD class extends CRUDBase with custom methods
- [ ] Custom exceptions for business logic errors
- [ ] Service layer with business validation
- [ ] Routes with proper error handling
- [ ] All components exported in `__init__.py`
- [ ] Router registered in main app
- [ ] Database migration created
- [ ] API tested

---

## Architecture Summary

```
┌─────────────────────────────────────────────────────────┐
│                    HTTP Request                          │
└──────────────────────┬──────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────┐
│  Routes Layer (routes.py)                                │
│  - Validate HTTP input                                   │
│  - Handle HTTP errors                                    │
│  - Return HTTP responses                                 │
└──────────────────────┬──────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────┐
│  Service Layer (services.py)                             │
│  - Business logic validation                             │
│  - Orchestrate CRUD operations                           │
│  - Throw custom exceptions                               │
└──────────────────────┬──────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────┐
│  CRUD Layer (crud.py)                                    │
│  - Database operations only                              │
│  - No business logic                                     │
│  - Return data or None                                   │
└──────────────────────┬──────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────┐
│  Models Layer (models.py)                                │
│  - Database schema definition                            │
│  - SQLAlchemy ORM                                        │
└─────────────────────────────────────────────────────────┘
```

---

## Tips

1. **Start Simple**: Begin with basic CRUD, add complexity later
2. **Keep It DRY**: Reuse CRUDBase methods when possible
3. **Validate Early**: Put validation in Schemas, then Services
4. **Separate Concerns**: Don't mix HTTP, business, and data logic
5. **Document Well**: Add docstrings and README for each module

---

**This structure is production-ready and scalable for enterprise applications.**

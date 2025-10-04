# FastAPI Learn - Architecture Guide

## Overview

This FastAPI application follows a modular, layered architecture inspired by Django's app structure. Each feature is organized into self-contained apps with clear separation of concerns.

## Project Structure

```
fastapi-learn/
├── app/
│   ├── core/                    # Core application components
│   │   ├── __init__.py
│   │   ├── main.py             # FastAPI app initialization and core routes
│   │   ├── database.py         # Database configuration and session management
│   │   ├── models.py           # Base SQLAlchemy model
│   │   ├── schemas.py          # Core shared schemas
│   │   └── crud.py             # Base CRUD class for reusability
│   └── product/                # Product feature app
│       ├── __init__.py
│       ├── models.py           # Product SQLAlchemy models
│       ├── schemas.py          # Product Pydantic schemas
│       ├── crud.py             # Product data access layer
│       ├── services.py         # Product business logic
│       ├── routes.py           # Product API endpoints
│       └── README.md           # Product app documentation
├── migrations/                  # Alembic database migrations
├── docker-compose.yml          # Container orchestration
├── Dockerfile                  # Container definition
├── pyproject.toml             # Project dependencies and configuration
├── README.md                  # Main project documentation
└── ARCHITECTURE.md            # This file
```

## Architecture Layers

### 1. Routes Layer (API)
**Location**: `app/{app_name}/routes.py`

**Responsibilities**:
- Handle HTTP requests and responses
- Input validation using Pydantic schemas
- Error handling and HTTP status codes
- Dependency injection (database sessions, authentication, etc.)
- API documentation via FastAPI

**Example**:
```python
@router.get("/", response_model=List[Product])
async def get_all_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    session: AsyncSession = Depends(get_session)
):
    products = await ProductService.get_all_products(session, skip, limit)
    return products
```

### 2. Service Layer (Business Logic)
**Location**: `app/{app_name}/services.py`

**Responsibilities**:
- Implement business rules and validation
- Coordinate between different CRUD operations
- Handle complex business workflows
- Provide a clean interface for the routes layer

**Example**:
```python
@staticmethod
async def create_product(session: AsyncSession, product_data: ProductCreate) -> ProductModel:
    # Business logic: Check if product name already exists
    existing_product = await product_crud.get_by_name(session, product_data.name)
    if existing_product:
        raise ValueError(f"Product with name '{product_data.name}' already exists")
    
    # Business logic: Validate minimum price
    if product_data.price < 0.01:
        raise ValueError("Product price must be at least $0.01")
    
    return await product_crud.create(session, obj_in=product_data)
```

### 3. CRUD Layer (Data Access)
**Location**: `app/{app_name}/crud.py`

**Responsibilities**:
- Direct database operations (Create, Read, Update, Delete)
- Query optimization and database-specific logic
- Data transformation between database and application models
- Extend the base CRUD class for common operations

**Example**:
```python
class ProductCRUD(CRUDBase[ProductModel, ProductCreate, ProductUpdate]):
    def __init__(self):
        super().__init__(ProductModel)

    async def get_by_name(self, session: AsyncSession, name: str) -> Optional[ProductModel]:
        result = await session.execute(
            select(ProductModel).where(ProductModel.name == name)
        )
        return result.scalar_one_or_none()
```

### 4. Models Layer (Data)
**Location**: `app/{app_name}/models.py`

**Responsibilities**:
- Define database schema using SQLAlchemy
- Relationships between tables
- Database constraints and indexes

### 5. Schemas Layer (Validation)
**Location**: `app/{app_name}/schemas.py`

**Responsibilities**:
- Input/output validation using Pydantic
- Data serialization/deserialization
- API documentation schema

## Core Components

### Database Management (`app/core/database.py`)
- Async SQLAlchemy engine and session management
- Connection pooling and configuration
- Database URL construction from environment variables
- Health check and startup verification

### Base CRUD (`app/core/crud.py`)
- Generic CRUD operations that can be inherited
- Type-safe operations using Python generics
- Common database patterns (pagination, filtering, etc.)

### Main Application (`app/core/main.py`)
- FastAPI app initialization
- Router registration
- Lifespan events (startup/shutdown)
- Core endpoints (health check, database test)

## Design Principles

### 1. Separation of Concerns
Each layer has a single responsibility:
- **Routes**: Handle HTTP protocol
- **Services**: Implement business logic
- **CRUD**: Manage data access
- **Models**: Define data structure

### 2. Dependency Inversion
Higher-level modules don't depend on lower-level modules. Both depend on abstractions:
- Services depend on CRUD interfaces, not implementations
- Routes depend on service interfaces
- Database sessions are injected as dependencies

### 3. Single Responsibility Principle
Each class and function has one reason to change:
- CRUD classes handle only data operations
- Service classes handle only business logic
- Route functions handle only HTTP concerns

### 4. Open/Closed Principle
The architecture is open for extension but closed for modification:
- New apps can be added without changing existing code
- Base CRUD class can be extended for specific needs
- New business rules can be added to services without changing CRUD

## Adding New Apps

To add a new feature app (e.g., `user`, `order`):

1. **Create app directory**: `app/new_app/`
2. **Add required files**:
   ```
   app/new_app/
   ├── __init__.py
   ├── models.py      # SQLAlchemy models
   ├── schemas.py     # Pydantic schemas
   ├── crud.py        # Data access layer
   ├── services.py    # Business logic
   ├── routes.py      # API endpoints
   └── README.md      # App documentation
   ```
3. **Register router** in `app/core/main.py`:
   ```python
   from app.new_app.routes import router as new_app_router
   app.include_router(new_app_router)
   ```
4. **Import models** in `migrations/env.py` for Alembic:
   ```python
   from app.new_app.models import NewModel  # noqa: F401
   ```

## Benefits

### Maintainability
- Clear separation makes code easier to understand and modify
- Changes in one layer don't affect others
- Business logic is centralized and testable

### Scalability
- New features can be added as separate apps
- Database operations are optimized in the CRUD layer
- Services can be easily cached or moved to separate microservices

### Testability
- Each layer can be tested independently
- Business logic can be tested without database
- CRUD operations can be tested with test databases

### Reusability
- Base CRUD class reduces code duplication
- Common patterns are abstracted
- Services can be reused across different interfaces (API, CLI, etc.)

## Best Practices

1. **Keep routes thin**: Move business logic to services
2. **Keep services focused**: One service per business domain
3. **Use type hints**: Leverage Python's type system for better IDE support
4. **Handle errors appropriately**: Use specific exceptions and proper HTTP status codes
5. **Document your APIs**: Use Pydantic schemas and FastAPI's automatic documentation
6. **Test each layer**: Unit tests for services, integration tests for routes
7. **Use dependency injection**: Makes code more testable and flexible
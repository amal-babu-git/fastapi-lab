# Database Setup

This document explains the complete database configuration including SQLAlchemy, Pydantic validation, Alembic migrations, and AsyncPG integration.

## Database Stack Overview

### Core Components
- **PostgreSQL 16** - Primary database
- **SQLAlchemy 2.0** - Async ORM with modern Python features
- **AsyncPG** - High-performance async PostgreSQL driver
- **Alembic** - Database migration management
- **Pydantic** - Data validation and serialization

## Database Configuration

### Connection Setup (`app/core/database.py`)

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

# Async engine configuration
engine = create_async_engine(
    DATABASE_URL,  # postgresql+asyncpg://user:pass@host:port/db
    echo=settings.DATABASE_ECHO,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
)

# Session factory
async_session = async_sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Base model class
class Base(DeclarativeBase):
    pass
```

### Environment Configuration (`.env`)

```bash
# Database connection
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=fastapi_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password

# Connection pool settings
DATABASE_POOL_SIZE=5
DATABASE_MAX_OVERFLOW=10
DATABASE_ECHO=false  # Set to true for SQL logging
```

## SQLAlchemy Models

### Base Model Pattern (`app/core/models.py`)

```python
from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from .database import Base

class BaseModel(AsyncAttrs, Base):
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

### Feature Model Example (`app/product/models.py`)

```python
from sqlalchemy import Column, String, Numeric, Text, Boolean
from app.core.models import BaseModel

class Product(BaseModel):
    __tablename__ = "products"
    
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}')>"
```

## Pydantic Schemas

### Schema Organization (`app/product/schemas.py`)

```python
from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from datetime import datetime
from typing import Optional

# Base schema with common config
class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

# Input schemas (for API requests)
class ProductCreate(BaseSchema):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    price: Decimal = Field(..., gt=0, decimal_places=2)
    is_active: bool = Field(default=True)

class ProductUpdate(BaseSchema):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    price: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    is_active: Optional[bool] = None

# Output schemas (for API responses)
class ProductResponse(BaseSchema):
    id: int
    name: str
    description: Optional[str]
    price: Decimal
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
```

### Schema Validation Features

- **Type Safety**: Automatic type conversion and validation
- **Field Constraints**: Min/max length, numeric ranges, regex patterns
- **Custom Validators**: Complex validation logic
- **Serialization**: Automatic conversion from SQLAlchemy models

## CRUD Operations

### Base CRUD Pattern (`app/core/crud.py`)

```python
from typing import Generic, TypeVar, Type, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from pydantic import BaseModel

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseCRUD(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    async def get(self, db: AsyncSession, id: int) -> Optional[ModelType]:
        result = await db.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()
    
    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[ModelType]:
        result = await db.execute(select(self.model).offset(skip).limit(limit))
        return result.scalars().all()
    
    async def create(self, db: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        obj_data = obj_in.model_dump()
        db_obj = self.model(**obj_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def update(self, db: AsyncSession, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        obj_data = obj_in.model_dump(exclude_unset=True)
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def delete(self, db: AsyncSession, id: int) -> bool:
        result = await db.execute(delete(self.model).where(self.model.id == id))
        await db.commit()
        return result.rowcount > 0
```

### Feature-Specific CRUD (`app/product/crud.py`)

```python
from app.core.crud import BaseCRUD
from .models import Product
from .schemas import ProductCreate, ProductUpdate

class ProductCRUD(BaseCRUD[Product, ProductCreate, ProductUpdate]):
    async def get_by_name(self, db: AsyncSession, name: str) -> Optional[Product]:
        result = await db.execute(select(Product).where(Product.name == name))
        return result.scalar_one_or_none()
    
    async def get_active_products(self, db: AsyncSession) -> List[Product]:
        result = await db.execute(select(Product).where(Product.is_active == True))
        return result.scalars().all()

# Create instance
product_crud = ProductCRUD(Product)
```

## Alembic Migrations

### Configuration (`alembic.ini`)

```ini
[alembic]
script_location = migrations
sqlalchemy.url = postgresql+asyncpg://user:pass@host:port/db

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic
```

### Migration Environment (`migrations/env.py`)

```python
import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
from app.core.database import Base
from app.core.settings import settings

# Import all models to ensure they're registered
from app.product.models import *  # noqa

config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata

def run_migrations_online() -> None:
    connectable = create_async_engine(
        settings.DATABASE_URL,
        poolclass=pool.NullPool,
    )

    async def do_run_migrations(connection: Connection) -> None:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()

    async def run_async_migrations() -> None:
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)
        await connectable.dispose()

    asyncio.run(run_async_migrations())

run_migrations_online()
```

### Common Migration Commands

```bash
# Create a new migration
alembic revision --autogenerate -m "Add product table"

# Apply migrations
alembic upgrade head

# Downgrade one revision
alembic downgrade -1

# Show current revision
alembic current

# Show migration history
alembic history
```

## AsyncPG Integration

### Connection Benefits
- **Performance**: Fastest PostgreSQL driver for Python
- **Async Support**: Native async/await support
- **Type Safety**: Proper type conversion
- **Connection Pooling**: Efficient resource management

### Usage in SQLAlchemy
```python
# URL format for AsyncPG
DATABASE_URL = "postgresql+asyncpg://user:password@host:port/database"

# Engine configuration optimized for AsyncPG
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=3600,   # Recycle connections every hour
)
```

## Database Session Management

### Dependency Injection Pattern

```python
# Session dependency
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

# Usage in routes
@router.post("/products/", response_model=ProductResponse)
async def create_product(
    product: ProductCreate,
    db: AsyncSession = Depends(get_db)
):
    return await product_crud.create(db, product)
```

### Transaction Management

```python
# Automatic transaction handling
async def create_product_with_related_data(db: AsyncSession, product_data: ProductCreate):
    try:
        # All operations in same transaction
        product = await product_crud.create(db, product_data)
        # Additional operations...
        await db.commit()  # Explicit commit if needed
        return product
    except Exception:
        await db.rollback()  # Automatic rollback on error
        raise
```

## Best Practices

### 1. Model Design
- Use `BaseModel` for common fields (id, timestamps)
- Add proper indexes for query performance
- Use appropriate column types and constraints
- Include `__repr__` methods for debugging

### 2. Schema Design
- Separate create/update/response schemas
- Use proper validation with Field constraints
- Configure `from_attributes=True` for ORM integration
- Handle optional fields appropriately

### 3. CRUD Operations
- Use generic base CRUD for common operations
- Add feature-specific methods in derived classes
- Handle exceptions properly
- Use proper type hints

### 4. Migration Management
- Always review auto-generated migrations
- Test migrations on development data
- Use descriptive migration messages
- Keep migrations small and focused

### 5. Performance
- Use connection pooling appropriately
- Add database indexes for frequent queries
- Use `select` with proper filtering
- Avoid N+1 query problems with eager loading

This database setup provides a robust, scalable foundation for data-driven applications with proper validation, migrations, and async performance.
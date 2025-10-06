# Architecture

This document explains the architectural patterns and design decisions used in this FastAPI base template.

## Overall Architecture

The application follows a **layered architecture** with clear separation of concerns:

```
┌─────────────────────────────────────────┐
│              API Layer                  │
│         (FastAPI Routes)                │
├─────────────────────────────────────────┤
│            Service Layer                │
│         (Business Logic)                │
├─────────────────────────────────────────┤
│             CRUD Layer                  │
│        (Database Operations)            │
├─────────────────────────────────────────┤
│             Model Layer                 │
│         (SQLAlchemy Models)             │
├─────────────────────────────────────────┤
│            Database Layer               │
│           (PostgreSQL)                  │
└─────────────────────────────────────────┘
```

## Core Components

### 1. FastAPI Application (`app/core/main.py`)
- Central application instance
- Middleware configuration
- Exception handler registration
- Router inclusion and API versioning

### 2. Database Layer (`app/core/database.py`)
- Async SQLAlchemy engine configuration
- Session management with dependency injection
- Connection pooling and lifecycle management

### 3. Settings Management (`app/core/settings.py`)
- Pydantic-based configuration
- Environment variable handling
- Type-safe settings with validation

### 4. Modular Design
Each feature module contains:
- **Models**: Database schema definition
- **Schemas**: API input/output validation
- **CRUD**: Database operation abstraction
- **Services**: Business logic implementation
- **Routes**: API endpoint definitions

## Design Patterns

### 1. Dependency Injection
```python
# Database session injection
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

# Usage in routes
@router.get("/products/")
async def get_products(db: AsyncSession = Depends(get_db)):
    return await product_service.get_all(db)
```

### 2. Repository Pattern (CRUD Layer)
```python
# Base CRUD operations
class BaseCRUD:
    async def get(self, db: AsyncSession, id: int)
    async def create(self, db: AsyncSession, obj_in: BaseModel)
    async def update(self, db: AsyncSession, db_obj, obj_in)
    async def delete(self, db: AsyncSession, id: int)
```

### 3. Service Layer Pattern
```python
# Business logic separation
class ProductService:
    def __init__(self, crud: ProductCRUD):
        self.crud = crud
    
    async def create_product_with_validation(self, db, product_data):
        # Business logic here
        return await self.crud.create(db, product_data)
```

### 4. Schema Validation
```python
# Input validation
class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: Decimal = Field(..., gt=0)

# Output serialization
class ProductResponse(BaseModel):
    id: int
    name: str
    price: Decimal
    created_at: datetime
```

## Async Architecture

### Database Operations
- All database operations are async using `asyncpg`
- Connection pooling for optimal performance
- Proper session lifecycle management

### Request Handling
- Async route handlers for non-blocking I/O
- Concurrent request processing
- Efficient resource utilization

## Error Handling Strategy

### 1. Layered Exception Handling
```python
# Custom exceptions
class ProductNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Product not found")

# Global exception handlers
@app.exception_handler(ProductNotFoundError)
async def product_not_found_handler(request, exc):
    return JSONResponse(status_code=404, content={"error": "Product not found"})
```

### 2. Validation Errors
- Automatic Pydantic validation
- Structured error responses
- Client-friendly error messages

## Security Architecture

### 1. Environment-based Configuration
- Sensitive data in environment variables
- No hardcoded secrets in code
- Separate configs for different environments

### 2. Database Security
- Connection pooling with proper limits
- SQL injection prevention through ORM
- Async operations for better resource management

## Scalability Considerations

### 1. Modular Structure
- Easy to add new features without affecting existing code
- Clear boundaries between modules
- Independent testing and deployment of modules

### 2. Database Design
- Async operations for high concurrency
- Proper indexing strategies
- Migration system for schema evolution

### 3. Containerization
- Docker for consistent environments
- Easy horizontal scaling
- Resource isolation and management

## Development Workflow

### 1. Code Organization
```
Feature Development Flow:
1. Define models (database schema)
2. Create schemas (API validation)
3. Implement CRUD operations
4. Add business logic in services
5. Create API routes
6. Write tests
7. Update documentation
```

### 2. Database Changes
```
Migration Workflow:
1. Modify models
2. Generate migration: alembic revision --autogenerate
3. Review migration file
4. Apply migration: alembic upgrade head
```

### 3. API Versioning
- Routes organized under `/api/v1/`
- Easy to add new versions without breaking existing clients
- Backward compatibility considerations

## Performance Optimizations

### 1. Database
- Async operations prevent blocking
- Connection pooling reduces overhead
- Lazy loading and eager loading strategies

### 2. API
- Automatic response caching headers
- Efficient serialization with Pydantic
- Minimal data transfer with proper schemas

### 3. Development
- Hot reload for fast development cycles
- Automatic API documentation generation
- Built-in debugging and logging

This architecture provides a solid foundation that can scale from small projects to large applications while maintaining code quality and developer productivity.
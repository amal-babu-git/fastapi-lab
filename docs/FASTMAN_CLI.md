# FastMan CLI

A Django-inspired management command tool for generating FastAPI modules with complete CRUD functionality.

## What is FastMan CLI?

FastMan CLI is a code generation tool that creates production-ready FastAPI modules following best practices. It generates all the necessary files for a complete feature module in seconds.

## Quick Start

### Generate a New Module

```bash
python manage.py startapp Product
```

This creates a complete `product` module with:
- Database models (SQLAlchemy)
- API schemas (Pydantic)
- CRUD operations
- Business logic services
- REST API routes
- Custom exceptions
- Documentation

### Generated Structure

```
app/product/
├── __init__.py         # Module exports
├── models.py          # SQLAlchemy database model
├── schemas.py         # Pydantic validation schemas
├── crud.py            # Database CRUD operations
├── services.py        # Business logic layer
├── routes.py          # FastAPI REST endpoints
├── exceptions.py      # Custom error handling
└── README.md          # Module documentation
```

## Generated Features

### Database Model
- Primary key with auto-increment
- Common fields (name, description, is_active)
- Timestamps (created_at, updated_at)
- Proper indexing and constraints

### API Schemas
- **Create Schema** - Input validation for new records
- **Update Schema** - Partial updates with optional fields
- **Response Schema** - Output serialization
- Type-safe with Pydantic validation

### CRUD Operations
- `get()` - Fetch single record
- `get_multi()` - List with pagination
- `create()` - Create new record
- `update()` - Update existing record
- `delete()` - Remove record
- `get_by_name()` - Custom query method
- `get_active()` - Filter active records

### REST API Endpoints
- `GET /products/` - List all products
- `GET /products/{id}` - Get product by ID
- `POST /products/` - Create new product
- `PUT /products/{id}` - Update product
- `DELETE /products/{id}` - Delete product
- `GET /products/name/{name}` - Get by name

### Business Logic
- Input validation and sanitization
- Duplicate checking
- Error handling with proper HTTP status codes
- Logging for debugging and monitoring

## Usage Examples

### Basic Module Creation
```bash
# Create a User module
python manage.py startapp User

# Create an Order module
python manage.py startapp Order

# Create a Category module
python manage.py startapp Category
```

### Advanced Options
```bash
# Force overwrite existing files
python manage.py startapp Product --force

# Specify custom directory
python manage.py startapp Customer --dir app

# Get help
python manage.py startapp --help
```

## After Generation Steps

### 1. Register the Router
Add to `app/apis/v1.py`:
```python
from app.product.routes import router as product_router

router.include_router(product_router)
```

### 2. Create Database Migration
```bash
alembic revision --autogenerate -m "Add product table"
alembic upgrade head
```

### 3. Test Your API
```bash
uvicorn app.core.main:app --reload
```
Visit `http://localhost:8000/docs` to see your new endpoints.

## Customization

### Modify Generated Code
After generation, customize the files:
- Add custom fields to `models.py`
- Extend validation in `schemas.py`
- Add business logic to `services.py`
- Create additional endpoints in `routes.py`

### Template Customization
Edit templates in `fastman_cli/templates/` to change the generated code structure.

## CLI Commands

### Available Commands
```bash
# Generate new module
python manage.py startapp <ModuleName>

# Show CLI version
python manage.py version

# Get help
python manage.py --help
```

### Command Options
- `--force` - Overwrite existing files
- `--dir` - Specify target directory
- `--help` - Show command help

## Benefits

### Development Speed
- Generate complete modules in seconds
- No boilerplate code writing
- Consistent code structure across modules

### Best Practices
- Follows FastAPI conventions
- Proper async/await patterns
- Type-safe code with full hints
- Separation of concerns (models, services, routes)

### Production Ready
- Error handling and validation
- Logging and monitoring hooks
- Scalable architecture patterns
- Documentation included

## Architecture Pattern

FastMan CLI generates modules following this pattern:

```
API Layer (routes.py)
    ↓
Service Layer (services.py)
    ↓
CRUD Layer (crud.py)
    ↓
Model Layer (models.py)
    ↓
Database (PostgreSQL)
```

This separation ensures:
- **Testability** - Each layer can be tested independently
- **Maintainability** - Clear responsibility boundaries
- **Scalability** - Easy to modify and extend
- **Reusability** - Services can be used by multiple routes

## Tips

1. **Use PascalCase** for module names (e.g., `ProductCategory`)
2. **Register routers** immediately after generation
3. **Run migrations** before testing
4. **Customize business logic** in the services layer
5. **Add relationships** between models as needed

FastMan CLI accelerates FastAPI development by eliminating repetitive setup tasks and ensuring consistent, high-quality code structure across your application.
# FastMan CLI

> A Django-like management command tool for FastAPI projects

FastMan CLI is a powerful code generation tool that creates complete, production-ready modular FastAPI applications following best practices and clean architecture principles.

## 🚀 Features

- **Complete Module Generation**: Creates all necessary files for a FastAPI module
- **Best Practices**: Follows FastAPI and SQLAlchemy best practices
- **Scalable Architecture**: Modular design with separation of concerns
- **Type-Safe**: Full type hints and Pydantic validation
- **Async by Default**: All database operations are asynchronous
- **Rich CLI**: Beautiful terminal output with progress indicators
- **Extensible**: Easy to add new commands

## 📋 Generated Structure

When you run `python manage.py startapp Product`, it generates:

```
app/product/
├── __init__.py         # Clean module exports
├── models.py          # SQLAlchemy model with Base fields
├── schemas.py         # Pydantic schemas (Create, Update, Response)
├── crud.py            # CRUD operations extending CRUDBase
├── services.py        # Business logic layer
├── routes.py          # FastAPI router with CRUD endpoints
├── exceptions.py      # Custom exceptions
└── README.md          # Module documentation
```

## 🛠️ Installation

1. **Install dependencies** (if not already installed):

```bash
pip install typer rich
```

Or add to your `pyproject.toml`:

```toml
[project]
dependencies = [
    "typer>=0.9.0",
    "rich>=13.0.0",
]
```

2. **Make manage.py executable** (optional, for Unix-like systems):

```bash
chmod +x manage.py
```

## 📖 Usage

### Basic Usage

Create a new module:

```bash
python manage.py startapp Order
```

This creates a new `order` module in the `app/` directory.

### Advanced Usage

Specify a custom directory:

```bash
python manage.py startapp Customer --dir app
```

Force overwrite existing files:

```bash
python manage.py startapp Product --force
```

Show version:

```bash
python manage.py version
```

Get help:

```bash
python manage.py --help
python manage.py startapp --help
```

## 📦 What Gets Generated

### 1. **Models** (`models.py`)

SQLAlchemy model with common fields:
- `id` - Primary key
- `name` - Indexed string field
- `description` - Optional text field
- `is_active` - Boolean for soft deletes
- `created_at` - Auto timestamp
- `updated_at` - Auto-updated timestamp

### 2. **Schemas** (`schemas.py`)

Pydantic models for validation:
- `{Model}Base` - Base schema
- `{Model}Create` - Creation schema
- `{Model}Update` - Update schema (all optional)
- `{Model}` - Response schema
- `{Model}InDB` - Database schema

### 3. **CRUD Operations** (`crud.py`)

Extends `CRUDBase` with custom methods:
- `get()`, `get_multi()` - Read operations
- `create()`, `update()` - Write operations
- `get_by_name()` - Custom query
- `get_active()` - Filter active records
- `deactivate()` - Soft delete

### 4. **Services** (`services.py`)

Business logic layer with:
- Input validation
- Duplicate checking
- Logging
- Exception handling

### 5. **Routes** (`routes.py`)

Complete REST API:
- `GET /{models}/` - List all
- `GET /{models}/{id}` - Get by ID
- `POST /{models}/` - Create
- `PUT /{models}/{id}` - Update
- `DELETE /{models}/{id}` - Delete (soft/hard)
- `GET /{models}/name/{name}` - Get by name

### 6. **Exceptions** (`exceptions.py`)

Custom exceptions for:
- Not found errors
- Already exists errors
- Invalid data errors

### 7. **Documentation** (`README.md`)

Comprehensive module documentation with:
- Architecture overview
- API reference
- Usage examples
- Testing guidelines

## 🔧 Post-Generation Steps

After generating a module, follow these steps:

### 1. Register the Router

Add to `app/apis/v1.py`:

```python
from app.order.routes import router as order_router

router = APIRouter(prefix="/v1")
router.include_router(order_router)
```

### 2. Create Database Migration

```bash
alembic revision --autogenerate -m "Add order table"
alembic upgrade head
```

### 3. Test Your API

```bash
uvicorn app.core.main:app --reload
```

Visit http://localhost:8000/docs to see your new endpoints!

### 4. Customize

Edit the generated files to add:
- Custom fields to models
- Business logic to services
- Additional endpoints to routes
- Relationships to other models

## 🎯 Examples

### Example 1: Create an Order Module

```bash
python manage.py startapp Order
```

**Result:**
```
✅ App 'Order' created successfully!

📊 Summary
App Name:      Order
Module Name:   order
Location:      d:\fastapi-learn\app\order
Files Created: 8
```

### Example 2: Create a Customer Module

```bash
python manage.py startapp customer
```

**Result:** Creates `app/customer/` with full CRUD structure

### Example 3: Create an Invoice Module

```bash
python manage.py startapp Invoice --dir app --force
```

**Result:** Creates `app/invoice/` and overwrites if exists

## 🏗️ Architecture

FastMan CLI follows a clean, modular architecture:

```
fastman_cli/
├── __init__.py              # Package initialization
├── cli.py                   # Main Typer app
├── commands/
│   ├── __init__.py
│   └── startapp.py         # Startapp command
├── templates/
│   ├── __init__.py
│   ├── model_template.py
│   ├── schema_template.py
│   ├── crud_template.py
│   ├── service_template.py
│   ├── route_template.py
│   ├── exception_template.py
│   ├── init_template.py
│   └── readme_template.py
└── utils/
    ├── __init__.py
    └── helpers.py          # String conversion utilities
```

### Adding New Commands

To add a new command:

1. Create `fastman_cli/commands/mycommand.py`:

```python
import typer
from rich.console import Console

console = Console()

def mycommand_command(arg: str):
    """My new command."""
    console.print(f"Running mycommand with: {arg}")
```

2. Register in `fastman_cli/cli.py`:

```python
from .commands.mycommand import mycommand_command

@app.command("mycommand")
def mycommand(arg: str):
    """Description of my command."""
    mycommand_command(arg)
```

3. Run it:

```bash
python manage.py mycommand "test"
```

## 🎨 Customization

### Customize Templates

Edit template files in `fastman_cli/templates/` to change the generated code structure.

### Customize Default Fields

Modify `model_template.py` to add/remove default fields:

```python
def generate_model(module_name: str, class_name: str) -> str:
    return f'''
    # Add your custom fields here
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    status: Mapped[str] = mapped_column(String(50), default="pending")
    '''
```

## 🧪 Testing

Test the CLI:

```bash
# Test help
python manage.py --help

# Test startapp
python manage.py startapp TestApp --dir app

# Verify files
ls app/testapp/
```

## 📚 Best Practices

1. **Always register routers** in `app/apis/v1.py` after generation
2. **Run migrations** after creating models
3. **Customize business logic** in services layer
4. **Add tests** for your modules
5. **Update documentation** as you modify code

## 🤝 Contributing

To contribute new commands or templates:

1. Follow the existing code structure
2. Add proper type hints
3. Include docstrings
4. Test thoroughly

## 📝 License

MIT License - feel free to use in your projects!

## 🙏 Acknowledgments

Inspired by Django's management commands and FastAPI's best practices.

---

**Happy coding! 🚀**

For issues or suggestions, please create an issue in the repository.

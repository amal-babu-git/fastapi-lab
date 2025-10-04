# FastMan CLI vs Django Management Commands

A side-by-side comparison showing how FastMan CLI brings Django's excellent developer experience to FastAPI.

## 🎯 Command Comparison

| Django | FastMan CLI | Description |
|--------|-------------|-------------|
| `python manage.py startapp myapp` | `python manage.py startapp MyApp` | Create new app/module |
| `python manage.py migrate` | *Future* | Run database migrations |
| `python manage.py makemigrations` | *Future* | Generate migrations |
| `python manage.py shell` | *Future* | Interactive shell |
| `python manage.py runserver` | `uvicorn app.core.main:app --reload` | Start dev server |
| `python manage.py createsuperuser` | *Future* | Create admin user |
| `python manage.py test` | *Future* | Run tests |

✅ = Currently implemented  
*Future* = Planned/can be added

## 📁 File Structure Comparison

### Django App Structure
```
myproject/
├── manage.py
├── myproject/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── myapp/
    ├── __init__.py
    ├── models.py         # Database models
    ├── views.py          # Request handlers
    ├── urls.py           # URL routing
    ├── admin.py          # Admin interface
    ├── apps.py           # App configuration
    └── migrations/       # Database migrations
```

### FastMan CLI Module Structure
```
fastapi-learn/
├── manage.py
├── app/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── main.py       # FastAPI app
│   │   ├── settings.py   # Configuration
│   │   ├── database.py   # DB connection
│   │   └── crud.py       # Base CRUD
│   └── myapp/
│       ├── __init__.py
│       ├── models.py     # SQLAlchemy models
│       ├── schemas.py    # Pydantic schemas
│       ├── routes.py     # API endpoints (≈ views.py)
│       ├── services.py   # Business logic
│       ├── crud.py       # Database operations
│       └── exceptions.py # Custom errors
└── migrations/           # Alembic migrations
```

## 🔄 Conceptual Mapping

| Django Concept | FastAPI + FastMan | Notes |
|----------------|-------------------|-------|
| **App** | **Module** | Self-contained feature |
| `models.Model` | `Base` (SQLAlchemy) | ORM models |
| `forms.Form` | Pydantic `BaseModel` | Validation |
| `views.View` | Route functions | Request handlers |
| `urls.py` | `router` | URL routing |
| `admin.py` | *Custom* | Admin interface |
| Django ORM | SQLAlchemy | Database ORM |
| `QuerySet` | SQLAlchemy `Query` | Database queries |
| Migrations | Alembic | Schema migrations |
| `settings.py` | `settings.py` | Configuration |
| Django REST Framework | FastAPI | API framework |

## 📝 Code Comparison

### Creating a Model

**Django:**
```python
# models.py
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'products'
        ordering = ['-created_at']
```

**FastMan CLI:**
```python
# models.py (Generated)
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class Product(Base):
    __tablename__ = "products"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, onupdate=datetime.utcnow)
```

### Creating a View/Endpoint

**Django:**
```python
# views.py
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
```

**FastMan CLI:**
```python
# routes.py (Generated)
from fastapi import APIRouter, Depends
from .schemas import Product, ProductCreate
from .services import ProductService

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/")
async def get_products(session: AsyncSession = Depends(get_session)):
    return await ProductService.get_all_products(session)

@router.post("/")
async def create_product(data: ProductCreate, session: AsyncSession = Depends(get_session)):
    return await ProductService.create_product(session, data)
```

### Validation

**Django:**
```python
# serializers.py
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'created_at']
        read_only_fields = ['id', 'created_at']
```

**FastMan CLI:**
```python
# schemas.py (Generated)
from pydantic import BaseModel, Field

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str = Field(None, max_length=1000)
    price: float = Field(..., gt=0)

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
```

## 🚀 Getting Started Comparison

### Django Workflow
```bash
# 1. Create project
django-admin startproject myproject
cd myproject

# 2. Create app
python manage.py startapp products

# 3. Define models in products/models.py
# 4. Add to INSTALLED_APPS in settings.py
# 5. Create migrations
python manage.py makemigrations

# 6. Run migrations
python manage.py migrate

# 7. Create views in products/views.py
# 8. Define URLs in products/urls.py
# 9. Include in main urls.py
# 10. Run server
python manage.py runserver
```

### FastMan CLI Workflow
```bash
# 1. Project already set up with core/

# 2. Create module
python manage.py startapp Product

# 3. Models, schemas, routes auto-generated!

# 4. Register router in app/apis/v1.py
# (Just add one import and one line)

# 5. Create migration
alembic revision --autogenerate -m "Add product"

# 6. Run migration
alembic upgrade head

# 7. Everything else already done!

# 8. Run server
uvicorn app.core.main:app --reload
```

**FastMan CLI saves ~5 steps!** ⚡

## 🎨 Development Experience

### Django
```python
# Manual setup required
✓ Create views.py
✓ Create serializers.py
✓ Create urls.py
✓ Wire up URLs
✓ Write boilerplate CRUD
✓ Handle exceptions
✓ Add logging
```

### FastMan CLI
```python
# All auto-generated!
✓ routes.py (views)
✓ schemas.py (serializers)
✓ services.py (business logic)
✓ crud.py (database operations)
✓ exceptions.py (error handling)
✓ Logging included
✓ Full CRUD endpoints
✓ Documentation generated
```

## 📊 Feature Parity

| Feature | Django | FastMan CLI |
|---------|--------|-------------|
| **Project scaffolding** | ✅ | ✅ |
| **App generation** | ✅ | ✅ |
| **ORM models** | ✅ | ✅ (SQLAlchemy) |
| **Migrations** | ✅ | ✅ (Alembic) |
| **Admin interface** | ✅ | ⚠️ (Can add) |
| **Authentication** | ✅ | ⚠️ (Can add) |
| **REST API** | ⚠️ (DRF) | ✅ (Built-in) |
| **Async support** | ⚠️ (Limited) | ✅ (Full) |
| **Type hints** | ⚠️ (Optional) | ✅ (Required) |
| **API docs** | ⚠️ (DRF) | ✅ (Auto) |
| **Validation** | ✅ | ✅ (Pydantic) |
| **Testing** | ✅ | ⚠️ (Manual) |

✅ = Full support  
⚠️ = Partial or manual

## 🎯 Philosophy Comparison

### Django Philosophy
- **Batteries included**: Everything you need out of the box
- **Convention over configuration**: Sensible defaults
- **DRY (Don't Repeat Yourself)**: Minimize code duplication
- **Explicit is better than implicit**: Clear code structure
- **Admin interface**: Built-in admin panel

### FastMan CLI Philosophy
- **Modular architecture**: Clean separation of concerns
- **Type-safe by default**: Full type hints everywhere
- **Async-first**: Modern async/await patterns
- **API-centric**: Built for REST APIs
- **Django-inspired**: Familiar commands and structure
- **Best practices**: Follows FastAPI conventions

## 💡 When to Use What

### Choose Django When:
- Building traditional web applications with templates
- Need built-in admin interface
- Want batteries-included framework
- Team familiar with Django
- Need mature ecosystem (packages, plugins)

### Choose FastAPI + FastMan When:
- Building REST APIs or microservices
- Need high performance (async)
- Want modern Python features (type hints)
- Prefer flexibility over conventions
- Need automatic API documentation
- Building real-time applications

## 🔄 Migration Path

### From Django to FastAPI + FastMan

1. **Study the structure**: Compare Django app to FastMan module
2. **Generate modules**: Use `startapp` for each Django app
3. **Copy models**: Convert Django models to SQLAlchemy
4. **Map views to routes**: Convert view functions to route handlers
5. **Convert serializers**: Django serializers → Pydantic schemas
6. **Migrate business logic**: Move to services layer
7. **Update tests**: Adapt Django tests to FastAPI
8. **Deploy**: Use async servers (Uvicorn, Hypercorn)

## 📚 Learning Curve

```
Django Developer → FastMan CLI
    │
    ├─ ✅ Familiar: manage.py commands
    ├─ ✅ Familiar: App/module structure  
    ├─ ✅ Familiar: Models concept
    ├─ 📖 Learn: Pydantic validation
    ├─ 📖 Learn: Async/await patterns
    ├─ 📖 Learn: Dependency injection
    └─ 📖 Learn: SQLAlchemy (if new)

Learning time: ~1-2 weeks for Django developers
```

## 🎁 Unique FastMan CLI Features

Features not in Django's `startapp`:

1. **Complete CRUD out of the box**: All endpoints generated
2. **Service layer**: Separation of business logic
3. **Exception handling**: Custom exceptions per module
4. **Logging**: Integrated logging setup
5. **Documentation**: Auto-generated README per module
6. **Type safety**: Full type hints everywhere
7. **Async-first**: All operations async
8. **Rich CLI**: Beautiful terminal output

## 🚀 Future Roadmap

Commands to add (inspired by Django):

```bash
python manage.py migrate          # Run Alembic migrations
python manage.py makemigrations   # Generate migrations
python manage.py shell           # IPython shell with app context
python manage.py dbshell         # PostgreSQL shell
python manage.py createsuperuser # Create admin user
python manage.py test            # Run pytest tests
python manage.py collectstatic   # For static files
python manage.py check           # Check for issues
```

## 📖 Resources

**Django:**
- Docs: https://docs.djangoproject.com
- Tutorial: https://docs.djangoproject.com/en/stable/intro/tutorial01/

**FastAPI + FastMan:**
- FastAPI: https://fastapi.tiangolo.com
- SQLAlchemy: https://docs.sqlalchemy.org
- Pydantic: https://docs.pydantic.dev
- FastMan CLI: `FASTMAN_CLI_GUIDE.md`

## ✨ Conclusion

FastMan CLI brings the best of Django's developer experience to FastAPI:

- ✅ **Familiar commands** (`startapp`, etc.)
- ✅ **Clean structure** (modular architecture)
- ✅ **Less boilerplate** (auto-generated code)
- ✅ **Modern stack** (async, type hints)
- ✅ **Best practices** (layered architecture)

**Perfect for Django developers moving to FastAPI!** 🎉

---

**Comparison Version**: 1.0.0  
**Last Updated**: 2025-10-04

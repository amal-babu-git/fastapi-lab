# API Router Pattern Guide

This document explains the standard routing pattern used in this FastAPI project.

## Architecture Overview

```
main.py
  └── /api
       └── v1.py (Version Router)
            ├── /products → product/routes.py
            ├── /users → user/routes.py (future)
            └── /orders → order/routes.py (future)
```

## The Three-Level Pattern

### Level 1: Module Routes (e.g., `app/product/routes.py`)

**Purpose**: Define endpoints for a specific business domain/module

**Rules**:
- ❌ **NO prefix** on the router
- ❌ **NO tags** on the router
- ✅ Only define the endpoints
- ✅ Keep it focused on one domain

**Example**:
```python
# app/product/routes.py
from fastapi import APIRouter

# Module router - clean, no configuration
router = APIRouter()

@router.get("/")
async def get_all_products():
    """Get all products"""
    pass

@router.post("/")
async def create_product():
    """Create a product"""
    pass

@router.get("/{product_id}")
async def get_product(product_id: int):
    """Get a single product"""
    pass
```

### Level 2: Version Router (e.g., `app/apis/v1.py`)

**Purpose**: Organize and version all module routers

**Rules**:
- ✅ Set version prefix (e.g., `/v1`, `/v2`)
- ❌ **NO tags** on the version router itself (to avoid duplication)
- ✅ Include module routers with their specific prefixes and tags
- ✅ This is where you define the API structure

**Example**:
```python
# app/apis/v1.py
from fastapi import APIRouter
from app.product.routes import router as product_router
from app.user.routes import router as user_router  # future module

# Version 1 API Router - NO tags to avoid duplication
router = APIRouter(prefix="/v1")

# Include module routers with their prefixes and tags
router.include_router(product_router, prefix="/products", tags=["Products"])
router.include_router(user_router, prefix="/users", tags=["Users"])  # future
```

### Level 3: Main Application (e.g., `app/core/main.py`)

**Purpose**: The root application that includes version routers

**Rules**:
- ✅ Include version routers with base API prefix
- ✅ Keep it simple and clean

**Example**:
```python
# app/core/main.py
from fastapi import FastAPI
from app.apis.v1 import router as v1_api_router

app = FastAPI(title="FastAPI Learn", version="0.1.0")

# Include version routers
app.include_router(v1_api_router, prefix="/api")

# Root and utility endpoints
@app.get("/")
def root():
    return {"message": "Welcome!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
```

## Final URL Structure

With this pattern, your endpoints will be:

```
/                           → Root endpoint
/health                     → Health check
/api/v1/products/           → List all products
/api/v1/products/{id}       → Get specific product
/api/v1/products/low-stock  → Custom product endpoint
/api/v1/users/              → Future: List all users
/api/v1/orders/             → Future: List all orders
```

## Benefits of This Pattern

1. **Clean Separation of Concerns**
   - Module routes focus only on endpoints
   - Version router handles organization
   - Main app stays minimal

2. **Easy Versioning**
   - Add `v2.py` for new API version
   - Keep `v1.py` unchanged for backward compatibility
   - Gradually migrate endpoints

3. **No Duplication**
   - Prefix and tags defined once per module
   - No conflicting configurations
   - Clear ownership

4. **Scalability**
   - Add new modules easily
   - Each module is self-contained
   - Easy to test in isolation

5. **Clear Documentation**
   - Swagger/OpenAPI groups endpoints by tags
   - Version separation is clear
   - No tag duplication

## Adding a New Module

To add a new module (e.g., `user`):

1. **Create the module structure**:
   ```
   app/user/
   ├── __init__.py
   ├── routes.py      # Define endpoints
   ├── models.py      # Database models
   ├── schemas.py     # Pydantic schemas
   ├── crud.py        # CRUD operations
   └── services.py    # Business logic
   ```

2. **Create router in `routes.py`** (no prefix/tags):
   ```python
   from fastapi import APIRouter
   
   router = APIRouter()
   
   @router.get("/")
   async def get_users():
       pass
   ```

3. **Include in `v1.py`** (with prefix/tags):
   ```python
   from app.user.routes import router as user_router
   
   router.include_router(user_router, prefix="/users", tags=["Users"])
   ```

4. **Done!** Your endpoints are now available at `/api/v1/users/`

## Future: API Versioning

When you need v2:

```python
# app/apis/v2.py
from fastapi import APIRouter
from app.product.routes import router as product_router
from app.user.routes import router as user_router

router = APIRouter(prefix="/v2", tags=["Version 2"])

# Maybe v2 products have different features
router.include_router(product_router, prefix="/products", tags=["Products v2"])
router.include_router(user_router, prefix="/users", tags=["Users v2"])
```

```python
# app/core/main.py
from app.apis.v1 import router as v1_api_router
from app.apis.v2 import router as v2_api_router

app.include_router(v1_api_router, prefix="/api")
app.include_router(v2_api_router, prefix="/api")
```

Now you have:
- `/api/v1/products/` → Version 1
- `/api/v2/products/` → Version 2

Both versions coexist!

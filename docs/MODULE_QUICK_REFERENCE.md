# Quick Reference: Adding New Modules

## Step-by-Step Guide

### 1. Create Module Structure

```bash
mkdir app/[module_name]
touch app/[module_name]/__init__.py
touch app/[module_name]/routes.py
touch app/[module_name]/models.py
touch app/[module_name]/schemas.py
touch app/[module_name]/crud.py
touch app/[module_name]/services.py
touch app/[module_name]/exceptions.py
```

### 2. Create Module Router (NO PREFIX/TAGS!)

**File**: `app/[module_name]/routes.py`

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from .schemas import [Model], [Model]Create, [Model]Update
from .services import [Model]Service

# ⚠️ IMPORTANT: No prefix, no tags!
router = APIRouter()


@router.get("/")
async def get_all_items(session: AsyncSession = Depends(get_session)):
    """Get all items"""
    return await [Model]Service.get_all(session)


@router.post("/")
async def create_item(
    item_in: [Model]Create,
    session: AsyncSession = Depends(get_session)
):
    """Create new item"""
    return await [Model]Service.create(session, item_in)


@router.get("/{item_id}")
async def get_item(item_id: int, session: AsyncSession = Depends(get_session)):
    """Get item by ID"""
    return await [Model]Service.get_by_id(session, item_id)
```

### 3. Register in Version Router (WITH PREFIX/TAGS!)

**File**: `app/apis/v1.py`

```python
from fastapi import APIRouter
from app.product.routes import router as product_router
from app.[module_name].routes import router as [module_name]_router  # ← Add import

# ⚠️ IMPORTANT: No tags on v1 router to avoid duplication!
router = APIRouter(prefix="/v1")

# Include module routers
router.include_router(product_router, prefix="/products", tags=["Products"])
router.include_router([module_name]_router, prefix="/[module_name]", tags=["[ModuleName]"])  # ← Add this
```

### 4. Test Your Endpoints

Your new endpoints are now available at:
- `GET /api/v1/[module_name]/`
- `POST /api/v1/[module_name]/`
- `GET /api/v1/[module_name]/{id}`

Check Swagger docs at: `http://localhost:8000/docs`

---

## Example: Adding a "User" Module

### Step 1: Create Structure
```bash
mkdir app/user
# Create files: __init__.py, routes.py, models.py, schemas.py, crud.py, services.py
```

### Step 2: Create Router (app/user/routes.py)
```python
from fastapi import APIRouter

router = APIRouter()  # ← No prefix!

@router.get("/")
async def get_users():
    return []
```

### Step 3: Register (app/apis/v1.py)
```python
from app.user.routes import router as user_router

router.include_router(user_router, prefix="/users", tags=["Users"])
```

### Step 4: Access
- URL: `http://localhost:8000/api/v1/users/`
- Swagger tag: "Users"

---

## Common Mistakes to Avoid

❌ **DON'T** add prefix in module router:
```python
# WRONG - in app/product/routes.py
router = APIRouter(prefix="/products")  # ← DON'T DO THIS!
```

❌ **DON'T** add tags in module router:
```python
# WRONG - in app/product/routes.py
router = APIRouter(tags=["Products"])  # ← DON'T DO THIS!
```

❌ **DON'T** add tags in version router:
```python
# WRONG - in app/apis/v1.py
router = APIRouter(prefix="/v1", tags=["Version 1"])  # ← DON'T DO THIS! Causes duplication
```

❌ **DON'T** forget to import in v1.py:
```python
# WRONG - in app/apis/v1.py
# Missing: from app.user.routes import router as user_router
router.include_router(user_router)  # ← Won't work, not imported!
```

✅ **DO** keep module routers clean:
```python
# CORRECT - in app/product/routes.py
router = APIRouter()  # ← Clean and simple!
```

✅ **DO** keep version router clean (no tags):
```python
# CORRECT - in app/apis/v1.py
router = APIRouter(prefix="/v1")  # ← Only prefix, no tags!
```

✅ **DO** add prefix/tags when including:
```python
# CORRECT - in app/apis/v1.py
router.include_router(product_router, prefix="/products", tags=["Products"])
```

---

## Checklist

When adding a new module, verify:

- [ ] Module router has NO prefix
- [ ] Module router has NO tags
- [ ] Imported in `v1.py`
- [ ] Included with proper prefix in `v1.py`
- [ ] Included with proper tags in `v1.py`
- [ ] Endpoints accessible at `/api/v1/[module]/`
- [ ] Swagger groups endpoints under correct tag
- [ ] No duplicate tags in Swagger docs

---

## Current Modules

| Module    | Prefix       | Tag        | Status |
|-----------|--------------|------------|--------|
| Product   | `/products`  | Products   | ✅ Active |
| User      | `/users`     | Users      | 🔜 Future |
| Order     | `/orders`    | Orders     | 🔜 Future |
| Category  | `/categories`| Categories | 🔜 Future |

# Router Configuration Cheat Sheet

## ❌ WRONG Configuration (Causes Duplicates)

### Version Router with Tags
```python
# app/apis/v1.py - WRONG!
router = APIRouter(prefix="/v1", tags=["Version 1"])  # ❌ Tags here cause duplication!
router.include_router(product_router, prefix="/products", tags=["Products"])
```

**Result in Swagger**: Endpoints appear TWICE
- Under "Version 1" tag
- Under "Products" tag

---

## ✅ CORRECT Configuration (No Duplicates)

### 1. Module Router (Clean)
```python
# app/product/routes.py
from fastapi import APIRouter

router = APIRouter()  # ✅ Nothing here!

@router.get("/")
async def get_products():
    pass
```

### 2. Version Router (Prefix Only)
```python
# app/apis/v1.py
from fastapi import APIRouter
from app.product.routes import router as product_router

router = APIRouter(prefix="/v1")  # ✅ Only prefix, NO tags!

# Tags added when including
router.include_router(product_router, prefix="/products", tags=["Products"])
```

### 3. Main App (Include Version Router)
```python
# app/core/main.py
from app.apis.v1 import router as v1_router

app = FastAPI()
app.include_router(v1_router, prefix="/api")
```

**Result in Swagger**: Endpoints appear ONCE
- Under "Products" tag only ✅

---

## Visual Flow

```
┌─────────────────────────────────────────┐
│ app/product/routes.py                   │
│                                         │
│ router = APIRouter()                    │
│   ├─ GET /                              │
│   ├─ POST /                             │
│   └─ GET /{id}                          │
│                                         │
│ 🏷️  Tags: NONE                          │
│ 📍 Prefix: NONE                         │
└────────────────┬────────────────────────┘
                 │
                 │ imported as product_router
                 ▼
┌─────────────────────────────────────────┐
│ app/apis/v1.py                          │
│                                         │
│ router = APIRouter(prefix="/v1")        │
│                                         │
│ router.include_router(                  │
│   product_router,                       │
│   prefix="/products",  ◄─── Added here  │
│   tags=["Products"]    ◄─── Added here  │
│ )                                       │
│                                         │
│ 🏷️  Tags: NONE (important!)             │
│ 📍 Prefix: /v1                          │
└────────────────┬────────────────────────┘
                 │
                 │ imported as v1_router
                 ▼
┌─────────────────────────────────────────┐
│ app/core/main.py                        │
│                                         │
│ app = FastAPI()                         │
│                                         │
│ app.include_router(                     │
│   v1_router,                            │
│   prefix="/api"        ◄─── Added here  │
│ )                                       │
│                                         │
│ Final URLs: /api/v1/products/*          │
│ Final Tags: ["Products"]                │
└─────────────────────────────────────────┘
```

---

## Tag Propagation Rules

### When you set tags on parent router:
```python
# Parent router
router = APIRouter(tags=["ParentTag"])

# Child router included
router.include_router(child, tags=["ChildTag"])

# Result: Endpoints get BOTH tags!
# - ParentTag ❌ (unwanted duplication)
# - ChildTag ✅
```

### Solution: Never set tags on parent router
```python
# Parent router
router = APIRouter()  # ✅ No tags!

# Child router included
router.include_router(child, tags=["ChildTag"])

# Result: Endpoints get ONE tag!
# - ChildTag ✅ (perfect!)
```

---

## Quick Checklist

Before you run your app, verify:

### Module Routers (product/routes.py)
- [ ] `router = APIRouter()` with no arguments
- [ ] No `prefix` parameter
- [ ] No `tags` parameter

### Version Routers (apis/v1.py)
- [ ] `router = APIRouter(prefix="/v1")` 
- [ ] Has `prefix` parameter ✅
- [ ] **NO** `tags` parameter ❌
- [ ] Each `include_router()` has both `prefix` and `tags`

### Main App (core/main.py)
- [ ] `app.include_router(v1_router, prefix="/api")`
- [ ] Only adds base API prefix

---

## Testing

After fixing, verify in Swagger docs (`/docs`):

✅ **Expected**: Each endpoint appears once
- Products section: All product endpoints
- default section: Root, health, db-test

❌ **If you see duplicates**: 
1. Check v1.py - remove tags from `APIRouter()` line
2. Check product/routes.py - remove prefix and tags
3. Restart your server

---

## Multiple Modules Example

```python
# app/apis/v1.py
from fastapi import APIRouter
from app.product.routes import router as product_router
from app.user.routes import router as user_router
from app.order.routes import router as order_router

# NO tags here!
router = APIRouter(prefix="/v1")

# Tags added per module
router.include_router(product_router, prefix="/products", tags=["Products"])
router.include_router(user_router, prefix="/users", tags=["Users"])
router.include_router(order_router, prefix="/orders", tags=["Orders"])
```

**Swagger Result**:
- Products: Product endpoints
- Users: User endpoints
- Orders: Order endpoints
- default: Root endpoints

No duplicates! 🎉

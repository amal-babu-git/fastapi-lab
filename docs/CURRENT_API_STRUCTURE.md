# Current API Structure

## URL Mapping

```
http://localhost:8000/
│
├── /                                    → Root welcome message
├── /health                              → Health check endpoint
├── /db-test                            → Database connectivity test
│
└── /api                                 → API base (from main.py)
    └── /v1                              → Version 1 (from v1.py)
        └── /products                    → Products module (from product/routes.py)
            ├── GET    /                 → Get all products (with pagination)
            ├── POST   /                 → Create a new product
            ├── GET    /stats            → Get product statistics
            ├── GET    /low-stock        → Get low stock products
            ├── GET    /search           → Search products by name
            ├── GET    /price-range      → Get products in price range
            ├── GET    /{product_id}     → Get product by ID
            ├── PUT    /{product_id}     → Update a product
            └── DELETE /{product_id}     → Delete a product
```

## Full Endpoint URLs

| Method | Endpoint                                    | Description                |
|--------|---------------------------------------------|----------------------------|
| GET    | `/api/v1/products/`                         | List all products          |
| POST   | `/api/v1/products/`                         | Create product             |
| GET    | `/api/v1/products/{id}`                     | Get product by ID          |
| PUT    | `/api/v1/products/{id}`                     | Update product             |
| DELETE | `/api/v1/products/{id}`                     | Delete product             |
| GET    | `/api/v1/products/stats`                    | Product statistics         |
| GET    | `/api/v1/products/low-stock?threshold=10`   | Low stock products         |
| GET    | `/api/v1/products/search?name=laptop`       | Search products            |
| GET    | `/api/v1/products/price-range?min=10&max=100` | Products in price range |

## OpenAPI/Swagger Tags

Your Swagger docs will show these sections:

- **Products**: All product-related endpoints (no duplication!)
- **default**: Root endpoints (/, /health, /db-test)

✅ Clean organization with no duplicate endpoint listings!

## File Responsibility

```
app/core/main.py
  → Registers: /api/v1/*
  → Includes: v1_api_router with prefix="/api"

app/apis/v1.py
  → Router: APIRouter(prefix="/v1")  ← NO TAGS (avoids duplication)
  → Includes: product_router with prefix="/products" and tags=["Products"]

app/product/routes.py
  → Router: APIRouter()  ← NO prefix, NO tags (clean module router)
  → Defines: All product endpoints (/, /{id}, /stats, etc.)
```

## Pattern Summary

✅ **Module routers** (product/routes.py): Define endpoints only
✅ **Version routers** (apis/v1.py): Add prefixes and tags
✅ **Main app** (core/main.py): Include version routers

This ensures:
- No duplicate prefixes
- No duplicate tags
- Clean separation of concerns
- Easy to add new modules
- Easy to version the API

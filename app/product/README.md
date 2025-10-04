# Product Module

This is a modular FastAPI application module for handling product-related functionality following standard layered architecture patterns.

## Architecture

The module follows a clean layered architecture pattern:

```
Routes Layer (API) → Service Layer (Business Logic) → CRUD Layer (Data Access) → Database
```

## Structure

```
app/product/
├── __init__.py          # Package initialization & exports
├── models.py            # SQLAlchemy ORM models
├── schemas.py           # Pydantic schemas for validation
├── crud.py              # Data access layer (CRUD operations)
├── services.py          # Business logic layer
├── routes.py            # API endpoint definitions
├── exceptions.py        # Custom exception classes
└── README.md            # This file
```

## Components

### Models (`models.py`)
Defines the database schema using SQLAlchemy ORM.

- **`Product`**: SQLAlchemy model for product data storage
  - Fields: `id`, `name`, `description`, `price`, `quantity`

### Schemas (`schemas.py`)
Pydantic models for request/response validation and serialization.

- **`ProductBase`**: Base schema with common fields and validation
- **`ProductCreate`**: Schema for creating products (inherits from ProductBase)
- **`ProductUpdate`**: Schema for partial updates (all fields optional)
- **`Product`**: Response schema with ID field

### CRUD (`crud.py`)
Data access layer - handles all direct database operations.

**`ProductCRUD`** class extends `CRUDBase` with:
- Standard CRUD operations:
  - `get(id)`: Get single product by ID
  - `get_multi(skip, limit)`: Get multiple products with pagination
  - `create(obj_in)`: Create new product
  - `update(db_obj, obj_in)`: Update existing product
  - `remove(id)`: Delete product
  - `count()`: Count total products
  
- Product-specific queries:
  - `get_by_name(name)`: Find product by name
  - `get_by_price_range(min_price, max_price)`: Filter by price range
  - `get_low_stock(threshold)`: Find products with low inventory

### Services (`services.py`)
Business logic layer - handles validation, business rules, and orchestrates CRUD operations.

**`ProductService`** class with static methods:
- `get_all_products(skip, limit)`: Retrieve all products with pagination
- `get_product_by_id(product_id)`: Get product by ID
- `create_product(product_data)`: Create new product with validation
  - Validates: unique name, minimum price
- `update_product(product_id, product_data)`: Update existing product
  - Validates: unique name (if changed), minimum price
- `delete_product(product_id)`: Delete product with checks
- `get_products_by_price_range(min_price, max_price)`: Filter by price
  - Validates: price range constraints
- `get_low_stock_products(threshold)`: Find low inventory items
  - Validates: non-negative threshold
- `update_stock(product_id, quantity_change)`: Update inventory
  - Validates: sufficient stock for reduction
- `get_product_stats()`: Get product statistics

### Exceptions (`exceptions.py`)
Custom exception classes for business logic errors:

- **`ProductException`**: Base exception for all product errors
- **`ProductNotFoundError`**: Product doesn't exist
- **`ProductAlreadyExistsError`**: Duplicate product name
- **`InvalidPriceError`**: Price below minimum ($0.01)
- **`InvalidPriceRangeError`**: Invalid price range parameters
- **`InsufficientStockError`**: Stock reduction exceeds available quantity
- **`InvalidStockThresholdError`**: Negative threshold value

### Routes (`routes.py`)
API endpoint definitions with proper error handling.

- Uses dependency injection for database sessions
- Catches specific exceptions and returns appropriate HTTP status codes
- Validates input using Pydantic schemas
- Returns structured JSON responses

## API Endpoints

### Basic CRUD
- `GET /products/` - Get all products (with pagination)
  - Query params: `skip`, `limit`
- `GET /products/{product_id}` - Get product by ID
  - Returns: 404 if not found
- `POST /products/` - Create new product
  - Returns: 201 on success, 400 for validation errors
- `PUT /products/{product_id}` - Update product
  - Returns: 404 if not found, 400 for validation errors
- `DELETE /products/{product_id}` - Delete product
  - Returns: 204 on success, 404 if not found

### Advanced Features
- `GET /products/stats` - Get product statistics
  - Returns: total products, low stock count
- `GET /products/low-stock` - Get products with low stock
  - Query param: `threshold` (default: 10)
- `GET /products/price-range` - Get products within price range
  - Query params: `min_price`, `max_price`
- `PATCH /products/{product_id}/stock` - Update product stock
  - Query param: `quantity_change` (can be positive or negative)
  - Returns: 400 if insufficient stock

## Business Rules

The service layer enforces these business rules:
- **Unique Names**: Product names must be unique
- **Minimum Price**: Prices must be at least $0.01
- **Non-Negative Stock**: Stock quantity cannot go below 0
- **Valid Price Ranges**: min_price ≤ max_price, both non-negative
- **Valid Thresholds**: Stock thresholds must be non-negative

## Error Handling

The module uses a three-tier error handling approach:

1. **Pydantic Validation** (Schemas): Type validation, field constraints
2. **Business Logic** (Services): Custom exceptions for business rule violations
3. **HTTP Layer** (Routes): Converts exceptions to appropriate HTTP responses

## Usage Example

```python
from app.product import router, ProductService

# In your main FastAPI app
app.include_router(router)

# Direct service usage
async def some_function(session: AsyncSession):
    product = await ProductService.get_product_by_id(session, product_id=1)
    return product
```

## Future Extensions

When adding new features to this module:

1. Add database operations to `crud.py`
2. Add business logic to `services.py`
3. Add custom exceptions to `exceptions.py` if needed
4. Add API endpoints to `routes.py`
5. Update schemas in `schemas.py` if needed
6. Export new components in `__init__.py`
- Price ranges must be valid (min ≤ max, non-negative)

## Usage

The product router is automatically included in the main FastAPI app. All endpoints are prefixed with `/products` and tagged as "products" for API documentation.

## Benefits of This Architecture

1. **Separation of Concerns**: Each layer has a specific responsibility
2. **Reusability**: CRUD operations can be reused across different services
3. **Testability**: Each layer can be tested independently
4. **Maintainability**: Business logic is centralized in the service layer
5. **Scalability**: Easy to add new features without affecting existing code
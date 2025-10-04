# Product App

This is a modular Django-style app for handling product-related functionality in the FastAPI application.

## Architecture

The app follows a layered architecture pattern:

```
Routes Layer (API) → Service Layer (Business Logic) → CRUD Layer (Data Access) → Database
```

## Structure

```
app/product/
├── __init__.py          # Package initialization
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic schemas for request/response
├── crud.py              # Data access layer (CRUD operations)
├── services.py          # Business logic layer
├── routes.py            # API endpoints
└── README.md           # This file
```

## Components

### Models (`models.py`)
- `Product`: SQLAlchemy model for product data storage

### Schemas (`schemas.py`)
- `ProductBase`: Base schema with common fields
- `ProductCreate`: Schema for creating products
- `ProductUpdate`: Schema for updating products (partial updates)
- `Product`: Response schema with ID

### CRUD (`crud.py`)
- `ProductCRUD`: Data access layer extending `CRUDBase`
- Handles all database operations
- Methods:
  - `get()`: Get by ID
  - `get_multi()`: Get multiple with pagination
  - `create()`: Create new record
  - `update()`: Update existing record
  - `remove()`: Delete record
  - `get_by_name()`: Get by product name
  - `get_by_price_range()`: Get products in price range
  - `get_low_stock()`: Get products with low stock

### Services (`services.py`)
- `ProductService`: Business logic layer
- Validates business rules before calling CRUD operations
- Methods:
  - `get_all_products()`: Retrieve all products with pagination
  - `get_product_by_id()`: Get product by ID
  - `create_product()`: Create new product with validation
  - `update_product()`: Update existing product with validation
  - `delete_product()`: Delete product with business checks
  - `get_products_by_price_range()`: Get products in price range
  - `get_low_stock_products()`: Get products with low stock
  - `update_stock()`: Update product stock with validation
  - `get_product_stats()`: Get product statistics

### Routes (`routes.py`)
- API endpoints with proper HTTP status codes
- Input validation using Pydantic schemas
- Error handling with appropriate HTTP exceptions
- Dependency injection for database sessions

## API Endpoints

### Basic CRUD
- `GET /products/` - Get all products (with pagination)
- `GET /products/{product_id}` - Get product by ID
- `POST /products/` - Create new product
- `PUT /products/{product_id}` - Update product
- `DELETE /products/{product_id}` - Delete product

### Advanced Features
- `GET /products/stats` - Get product statistics
- `GET /products/low-stock` - Get products with low stock
- `GET /products/price-range` - Get products within price range
- `PATCH /products/{product_id}/stock` - Update product stock

## Business Rules

The service layer enforces these business rules:
- Product names must be unique
- Product prices must be at least $0.01
- Stock cannot go below 0
- Price ranges must be valid (min ≤ max, non-negative)

## Usage

The product router is automatically included in the main FastAPI app. All endpoints are prefixed with `/products` and tagged as "products" for API documentation.

## Benefits of This Architecture

1. **Separation of Concerns**: Each layer has a specific responsibility
2. **Reusability**: CRUD operations can be reused across different services
3. **Testability**: Each layer can be tested independently
4. **Maintainability**: Business logic is centralized in the service layer
5. **Scalability**: Easy to add new features without affecting existing code
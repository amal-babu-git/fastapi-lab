# Product App

This is a modular Django-style app for handling product-related functionality in the FastAPI application.

## Structure

```
app/product/
├── __init__.py          # Package initialization
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic schemas for request/response
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

### Services (`services.py`)
- `ProductService`: Business logic layer with methods:
  - `get_all_products()`: Retrieve all products
  - `get_product_by_id()`: Get product by ID
  - `create_product()`: Create new product
  - `update_product()`: Update existing product
  - `delete_product()`: Delete product

### Routes (`routes.py`)
- API endpoints with proper HTTP status codes
- Input validation using Pydantic schemas
- Error handling with appropriate HTTP exceptions
- Dependency injection for database sessions

## API Endpoints

- `GET /products/` - Get all products
- `GET /products/{product_id}` - Get product by ID
- `POST /products/` - Create new product
- `PUT /products/{product_id}` - Update product
- `DELETE /products/{product_id}` - Delete product

## Usage

The product router is automatically included in the main FastAPI app. All endpoints are prefixed with `/products` and tagged as "products" for API documentation.
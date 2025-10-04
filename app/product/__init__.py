"""
Product module for managing product-related operations.

This module provides a complete CRUD implementation for products,
including models, schemas, services, and API routes.
"""

from .models import Product
from .schemas import ProductBase, ProductCreate, ProductUpdate, Product as ProductSchema
from .routes import router
from .services import ProductService
from .crud import product_crud
from .exceptions import (
    ProductException,
    ProductNotFoundError,
    ProductAlreadyExistsError,
    InvalidPriceError,
    InvalidPriceRangeError,
    InsufficientStockError,
    InvalidStockThresholdError,
)

__all__ = [
    "Product",
    "ProductBase",
    "ProductCreate",
    "ProductUpdate",
    "ProductSchema",
    "router",
    "ProductService",
    "product_crud",
    "ProductException",
    "ProductNotFoundError",
    "ProductAlreadyExistsError",
    "InvalidPriceError",
    "InvalidPriceRangeError",
    "InsufficientStockError",
    "InvalidStockThresholdError",
]

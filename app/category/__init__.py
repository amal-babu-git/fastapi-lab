"""
Category module for managing category-related operations.

This module provides a complete CRUD implementation for categorys,
including models, schemas, services, and API routes.
"""

from .models import Category
from .schemas import (
    CategoryBase,
    CategoryCreate,
    CategoryUpdate,
    Category as CategorySchema,
    CategoryInDB,
)
from .routes import router
from .services import CategoryService
from .crud import category_crud
from .exceptions import (
    CategoryException,
    CategoryNotFoundError,
    CategoryAlreadyExistsError,
    InvalidCategoryDataError,
)

__all__ = [
    "Category",
    "CategoryBase",
    "CategoryCreate",
    "CategoryUpdate",
    "CategorySchema",
    "CategoryInDB",
    "router",
    "CategoryService",
    "category_crud",
    "CategoryException",
    "CategoryNotFoundError",
    "CategoryAlreadyExistsError",
    "InvalidCategoryDataError",
]

"""__init__.py template generator."""


def generate_init(module_name: str, class_name: str) -> str:
    """Generate __init__.py file for module."""
    return f'''"""
{class_name} module for managing {module_name}-related operations.

This module provides a complete CRUD implementation for {module_name}s,
including models, schemas, services, and API routes.
"""

from .models import {class_name}
from .schemas import (
    {class_name}Base,
    {class_name}Create,
    {class_name}Update,
    {class_name} as {class_name}Schema,
    {class_name}InDB,
)
from .routes import router
from .services import {class_name}Service
from .crud import {module_name}_crud
from .exceptions import (
    {class_name}Exception,
    {class_name}NotFoundError,
    {class_name}AlreadyExistsError,
    Invalid{class_name}DataError,
)

__all__ = [
    "{class_name}",
    "{class_name}Base",
    "{class_name}Create",
    "{class_name}Update",
    "{class_name}Schema",
    "{class_name}InDB",
    "router",
    "{class_name}Service",
    "{module_name}_crud",
    "{class_name}Exception",
    "{class_name}NotFoundError",
    "{class_name}AlreadyExistsError",
    "Invalid{class_name}DataError",
]
'''

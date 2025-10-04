"""CRUD template generator."""


def generate_crud(module_name: str, class_name: str) -> str:
    """Generate CRUD operations file."""
    return f'''from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.crud import CRUDBase
from .models import {class_name} as {class_name}Model
from .schemas import {class_name}Create, {class_name}Update


class {class_name}CRUD(CRUDBase[{class_name}Model, {class_name}Create, {class_name}Update]):
    """CRUD operations for {class_name} model."""

    def __init__(self):
        super().__init__({class_name}Model)


# Create a singleton instance
{module_name}_crud = {class_name}CRUD()
'''

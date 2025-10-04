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

    async def get_by_name(
        self, 
        session: AsyncSession, 
        name: str
    ) -> Optional[{class_name}Model]:
        """Get a {module_name} by name."""
        result = await session.execute(
            select({class_name}Model).where({class_name}Model.name == name)
        )
        return result.scalar_one_or_none()

    async def get_active(
        self, 
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> List[{class_name}Model]:
        """Get all active {module_name}s."""
        result = await session.execute(
            select({class_name}Model)
            .where({class_name}Model.is_active == True)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def deactivate(
        self, 
        session: AsyncSession, 
        id: int
    ) -> Optional[{class_name}Model]:
        """Deactivate a {module_name} (soft delete)."""
        obj = await self.get(session, id)
        if obj:
            obj.is_active = False
            await session.commit()
            await session.refresh(obj)
        return obj


# Create a singleton instance
{module_name}_crud = {class_name}CRUD()
'''

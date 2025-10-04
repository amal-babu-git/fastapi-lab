from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.crud import CRUDBase
from .models import Category as CategoryModel
from .schemas import CategoryCreate, CategoryUpdate


class CategoryCRUD(CRUDBase[CategoryModel, CategoryCreate, CategoryUpdate]):
    """CRUD operations for Category model."""

    def __init__(self):
        super().__init__(CategoryModel)

    async def get_by_name(
        self, 
        session: AsyncSession, 
        name: str
    ) -> Optional[CategoryModel]:
        """Get a category by name."""
        result = await session.execute(
            select(CategoryModel).where(CategoryModel.name == name)
        )
        return result.scalar_one_or_none()

    async def get_active(
        self, 
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> List[CategoryModel]:
        """Get all active categorys."""
        result = await session.execute(
            select(CategoryModel)
            .where(CategoryModel.is_active == True)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def deactivate(
        self, 
        session: AsyncSession, 
        id: int
    ) -> Optional[CategoryModel]:
        """Deactivate a category (soft delete)."""
        obj = await self.get(session, id)
        if obj:
            obj.is_active = False
            await session.commit()
            await session.refresh(obj)
        return obj


# Create a singleton instance
category_crud = CategoryCRUD()

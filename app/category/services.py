from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.logging import get_logger
from .models import Category as CategoryModel
from .schemas import CategoryCreate, CategoryUpdate
from .crud import category_crud
from .exceptions import (
    CategoryAlreadyExistsError,
    CategoryNotFoundError,
)

# Configure logging
logger = get_logger(__name__)


class CategoryService:
    """Service layer for category business logic."""

    @staticmethod
    async def get_all_categorys(
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        active_only: bool = False
    ) -> List[CategoryModel]:
        """Get all categorys with pagination."""
        if active_only:
            return await category_crud.get_active(session, skip=skip, limit=limit)
        return await category_crud.get_multi(session, skip=skip, limit=limit)

    @staticmethod
    async def get_category_by_id(
        session: AsyncSession, 
        category_id: int
    ) -> CategoryModel:
        """Get a category by ID."""
        category = await category_crud.get(session, category_id)
        if not category:
            logger.warning(f"Category not found: {category_id}")
            raise CategoryNotFoundError(category_id)
        return category

    @staticmethod
    async def create_category(
        session: AsyncSession, 
        category_data: CategoryCreate
    ) -> CategoryModel:
        """Create a new category with business logic validation."""
        # Business logic: Check if category name already exists
        existing_category = await category_crud.get_by_name(
            session, 
            category_data.name
        )
        if existing_category:
            logger.warning(
                f"Category already exists: {category_data.name}"
            )
            raise CategoryAlreadyExistsError(category_data.name)

        logger.info(f"Creating category: {category_data.name}")
        category = await category_crud.create(session, obj_in=category_data)
        logger.info(f"Category created successfully: {category.id}")
        return category

    @staticmethod
    async def update_category(
        session: AsyncSession,
        category_id: int,
        category_data: CategoryUpdate
    ) -> CategoryModel:
        """Update an existing category."""
        category = await CategoryService.get_category_by_id(session, category_id)
        
        # Check if name is being changed and if it conflicts
        if category_data.name and category_data.name != category.name:
            existing = await category_crud.get_by_name(session, category_data.name)
            if existing:
                raise CategoryAlreadyExistsError(category_data.name)
        
        logger.info(f"Updating category: {category_id}")
        updated_category = await category_crud.update(
            session, 
            db_obj=category, 
            obj_in=category_data
        )
        logger.info(f"Category updated successfully: {category_id}")
        return updated_category

    @staticmethod
    async def delete_category(
        session: AsyncSession, 
        category_id: int,
        soft_delete: bool = True
    ) -> None:
        """Delete a category (soft delete by default)."""
        category = await CategoryService.get_category_by_id(session, category_id)
        
        if soft_delete:
            logger.info(f"Soft deleting category: {category_id}")
            await category_crud.deactivate(session, category_id)
        else:
            logger.warning(f"Hard deleting category: {category_id}")
            await category_crud.remove(session, id=category_id)
        
        logger.info(f"Category deleted successfully: {category_id}")

    @staticmethod
    async def get_category_by_name(
        session: AsyncSession, 
        name: str
    ) -> Optional[CategoryModel]:
        """Get a category by name."""
        return await category_crud.get_by_name(session, name)

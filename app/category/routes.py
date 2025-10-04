from fastapi import APIRouter, Depends, status, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_session
from app.core.logging import get_logger
from .schemas import Category, CategoryCreate, CategoryUpdate
from .services import CategoryService
from .exceptions import CategoryException

# Configure logging
logger = get_logger(__name__)

# Module router - no prefix/tags (handled by version router)
router = APIRouter(prefix="/categorys", tags=["Categorys"])


@router.get("/", response_model=List[Category])
async def get_all_categorys(
    skip: int = Query(0, ge=0, description="Number of categorys to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of categorys to return"),
    active_only: bool = Query(False, description="Return only active categorys"),
    session: AsyncSession = Depends(get_session)
):
    """Get all categorys with pagination."""
    try:
        categorys = await CategoryService.get_all_categorys(
            session, 
            skip, 
            limit,
            active_only
        )
        return categorys
    except CategoryException as e:
        logger.error(f"Error getting categorys: {e}")
        raise


@router.get("/{category_id}", response_model=Category)
async def get_category(
    category_id: int = Path(..., gt=0, description="Category ID"),
    session: AsyncSession = Depends(get_session)
):
    """Get a specific category by ID."""
    try:
        category = await CategoryService.get_category_by_id(session, category_id)
        return category
    except CategoryException as e:
        logger.error(f"Error getting category {category_id}: {e}")
        raise


@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: CategoryCreate,
    session: AsyncSession = Depends(get_session)
):
    """Create a new category."""
    try:
        category = await CategoryService.create_category(session, category_data)
        return category
    except CategoryException as e:
        logger.error(f"Error creating category: {e}")
        raise


@router.put("/{category_id}", response_model=Category)
async def update_category(
    category_id: int = Path(..., gt=0, description="Category ID"),
    category_data: CategoryUpdate = ...,
    session: AsyncSession = Depends(get_session)
):
    """Update an existing category."""
    try:
        category = await CategoryService.update_category(
            session, 
            category_id, 
            category_data
        )
        return category
    except CategoryException as e:
        logger.error(f"Error updating category {category_id}: {e}")
        raise


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int = Path(..., gt=0, description="Category ID"),
    soft_delete: bool = Query(True, description="Soft delete (deactivate) or hard delete"),
    session: AsyncSession = Depends(get_session)
):
    """Delete a category (soft delete by default)."""
    try:
        await CategoryService.delete_category(session, category_id, soft_delete)
    except CategoryException as e:
        logger.error(f"Error deleting category {category_id}: {e}")
        raise


@router.get("/name/{name}", response_model=Category)
async def get_category_by_name(
    name: str = Path(..., description="Category name"),
    session: AsyncSession = Depends(get_session)
):
    """Get a category by name."""
    try:
        category = await CategoryService.get_category_by_name(session, name)
        if not category:
            from .exceptions import CategoryNotFoundError
            raise CategoryNotFoundError(name)
        return category
    except CategoryException as e:
        logger.error(f"Error getting category by name {name}: {e}")
        raise

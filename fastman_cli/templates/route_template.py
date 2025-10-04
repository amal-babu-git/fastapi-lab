"""Route template generator."""


def generate_routes(module_name: str, class_name: str) -> str:
    """Generate API routes file."""
    return f'''from fastapi import APIRouter, Depends, status, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_session
from app.core.logging import get_logger
from .schemas import {class_name}, {class_name}Create, {class_name}Update
from .services import {class_name}Service
from .exceptions import {class_name}Exception

# Configure logging
logger = get_logger(__name__)

# Module router - no prefix/tags (handled by version router)
router = APIRouter(prefix="/{module_name}s", tags=["{class_name}s"])


@router.get("/", response_model=List[{class_name}])
async def get_all_{module_name}s(
    skip: int = Query(0, ge=0, description="Number of {module_name}s to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of {module_name}s to return"),
    session: AsyncSession = Depends(get_session)
):
    """Get all {module_name}s with pagination."""
    try:
        {module_name}s = await {class_name}Service.get_all_{module_name}s(
            session, 
            skip, 
            limit
        )
        return {module_name}s
    except {class_name}Exception as e:
        logger.error(f"Error getting {module_name}s: {{e}}")
        raise


@router.get("/{{{module_name}_id}}", response_model={class_name})
async def get_{module_name}(
    {module_name}_id: str = Path(..., description="{class_name} ID"),
    session: AsyncSession = Depends(get_session)
):
    """Get a specific {module_name} by ID."""
    try:
        {module_name} = await {class_name}Service.get_{module_name}_by_id(session, {module_name}_id)
        return {module_name}
    except {class_name}Exception as e:
        logger.error(f"Error getting {module_name} {{{module_name}_id}}: {{e}}")
        raise


@router.post("/", response_model={class_name}, status_code=status.HTTP_201_CREATED)
async def create_{module_name}(
    {module_name}_data: {class_name}Create,
    session: AsyncSession = Depends(get_session)
):
    """Create a new {module_name}."""
    try:
        {module_name} = await {class_name}Service.create_{module_name}(session, {module_name}_data)
        return {module_name}
    except {class_name}Exception as e:
        logger.error(f"Error creating {module_name}: {{e}}")
        raise


@router.put("/{{{module_name}_id}}", response_model={class_name})
async def update_{module_name}(
    {module_name}_id: str = Path(..., description="{class_name} ID"),
    {module_name}_data: {class_name}Update = ...,
    session: AsyncSession = Depends(get_session)
):
    """Update an existing {module_name}."""
    try:
        {module_name} = await {class_name}Service.update_{module_name}(
            session, 
            {module_name}_id, 
            {module_name}_data
        )
        return {module_name}
    except {class_name}Exception as e:
        logger.error(f"Error updating {module_name} {{{module_name}_id}}: {{e}}")
        raise


@router.delete("/{{{module_name}_id}}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_{module_name}(
    {module_name}_id: str = Path(..., description="{class_name} ID"),
    session: AsyncSession = Depends(get_session)
):
    """Delete a {module_name}."""
    try:
        await {class_name}Service.delete_{module_name}(session, {module_name}_id)
    except {class_name}Exception as e:
        logger.error(f"Error deleting {module_name} {{{module_name}_id}}: {{e}}")
        raise
'''

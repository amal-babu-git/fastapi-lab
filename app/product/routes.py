from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_session
from .schemas import Product, ProductCreate, ProductUpdate
from .services import ProductService

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=List[Product])
async def get_all_products(session: AsyncSession = Depends(get_session)):
    """Get all products."""
    products = await ProductService.get_all_products(session)
    return products


@router.get("/{product_id}", response_model=Product)
async def get_product_by_id(product_id: int, session: AsyncSession = Depends(get_session)):
    """Get a product by ID."""
    product = await ProductService.get_product_by_id(session, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product


@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate, 
    session: AsyncSession = Depends(get_session)
):
    """Create a new product."""
    try:
        product = await ProductService.create_product(session, product_data)
        return product
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create product: {str(e)}"
        )


@router.put("/{product_id}", response_model=Product)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    session: AsyncSession = Depends(get_session)
):
    """Update an existing product."""
    product = await ProductService.update_product(session, product_id, product_data)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, session: AsyncSession = Depends(get_session)):
    """Delete a product."""
    success = await ProductService.delete_product(session, product_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
# app/routers/products.py
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status, File, UploadFile, Form
from app.db.database import get_db
from app.services.products import ProductService
from sqlalchemy.orm import Session
from app.schemas.products import ProductCreate, ProductOut, ProductsOut, ProductOutDelete, ProductUpdate
from app.core.security import get_current_user, check_admin_role
import os

router = APIRouter(tags=["Products"], prefix="/products")


# Get All Products
@router.get("/", status_code=status.HTTP_200_OK, response_model=ProductsOut)
def get_all_products(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    search: str | None = Query("", description="Search based title of products"),
):
    return ProductService.get_all_products(db, page, limit, search)


# Get Product By ID
@router.get("/{product_id}", status_code=status.HTTP_200_OK, response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return ProductService.get_product(db, product_id)


# Create New Product
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ProductOut,
    dependencies=[Depends(check_admin_role)])
async def create_product(
        title: str = Form(...),
        description: Optional[str] = Form(None),
        price: int = Form(...),
        discount_percentage: float = Form(...),
        rating: float = Form(...),
        stock: int = Form(...),
        brand: str = Form(...),
        category_id: int = Form(...),
        thumbnail: UploadFile = File(None),
        images: List[UploadFile] = File([]),
        db: Session = Depends(get_db)):
    
    product = ProductCreate(
        title=title,
        description=description,
        price=price,
        discount_percentage=discount_percentage,
        rating=rating,
        stock=stock,
        brand=brand,
        category_id=category_id,
        thumbnail=thumbnail,
        images=images
    )
    return await ProductService.create_product(db, product)


# Update Exist Product
@router.put(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProductOut,
    dependencies=[Depends(check_admin_role)])
def update_product(
        product_id: int,
        updated_product: ProductUpdate,
        db: Session = Depends(get_db)):
    return ProductService.update_product(db, product_id, updated_product)


# Delete Product By ID
@router.delete(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProductOutDelete,
    dependencies=[Depends(check_admin_role)])
def delete_product(
        product_id: int,
        db: Session = Depends(get_db)):
    return ProductService.delete_product(db, product_id)

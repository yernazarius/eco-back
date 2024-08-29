from fastapi import APIRouter, Depends, Query, status
from app.db.database import get_db
from app.services.brand import BrandService
from sqlalchemy.orm import Session
from app.schemas.brand import BrandCreate, BrandOut, BrandsOut, BrandOutDelete, BrandUpdate
from app.core.security import check_admin_role


router = APIRouter(tags=["Brands"], prefix="/brands")


# Get All Categories
@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=BrandsOut)
def get_all_categories(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    search: str | None = Query("", description="Search based name of brands"),
):
    return BrandService.get_all_brands(db, page, limit, search)


# Get Category By ID
@router.get(
    "/{child_category_id}",
    status_code=status.HTTP_200_OK,
    response_model=BrandOut)
def get_category(child_category_id: int, db: Session = Depends(get_db)):
    return BrandService.get_brand(db, child_category_id)


# Create New Category
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=BrandOut,
    dependencies=[Depends(check_admin_role)])
def create_category(category: BrandCreate, db: Session = Depends(get_db)):
    return BrandService.create_brand(db, category)




# Update Existing Category
@router.put(
    "/{child_category_id}",
    status_code=status.HTTP_200_OK,
    response_model=BrandOut,
    dependencies=[Depends(check_admin_role)])
def update_category(child_category_id: int, updated_category: BrandUpdate, db: Session = Depends(get_db)):
    return BrandService.update_brand(db, child_category_id, updated_category)


# Delete Category By ID
@router.delete(
    "/{child_category_id}",
    status_code=status.HTTP_200_OK,
    response_model=BrandOutDelete,
    dependencies=[Depends(check_admin_role)])
def delete_category(child_category_id: int, db: Session = Depends(get_db)):
    return BrandService.delete_brand(db, child_category_id)

from fastapi import APIRouter, Depends, Query, status
from app.db.database import get_db
from app.services.category_grand import GrandCategoryService
from sqlalchemy.orm import Session
from app.schemas.category_grand import GrandCategoryCreate, GrandCategoryOut, GrandCategoriesOut, GrandCategoryOutDelete, GrandCategoryUpdate
from app.core.security import check_admin_role


router = APIRouter(tags=["Grand Categories"], prefix="/category_grand")


# Get All Categories
@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=GrandCategoriesOut)
def get_all_categories(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    search: str | None = Query("", description="Search based name of grand categories"),
):
    return GrandCategoryService.get_all_categories(db, page, limit, search)


# Get Category By ID
@router.get(
    "/{grand_category_id}",
    status_code=status.HTTP_200_OK,
    response_model=GrandCategoryOut)
def get_category(grand_category_id: int, db: Session = Depends(get_db)):
    return GrandCategoryService.get_category(db, grand_category_id)


# Create New Category
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=GrandCategoryOut,
    dependencies=[Depends(check_admin_role)])
def create_category(category: GrandCategoryCreate, db: Session = Depends(get_db)):
    return GrandCategoryService.create_category(db, category)


# Update Existing Category
@router.put(
    "/{grand_category_id}",
    status_code=status.HTTP_200_OK,
    response_model=GrandCategoryOut,
    dependencies=[Depends(check_admin_role)])
def update_category(grand_category_id: int, updated_category: GrandCategoryUpdate, db: Session = Depends(get_db)):
    return GrandCategoryService.update_category(db, grand_category_id, updated_category)


# Delete Category By ID
@router.delete(
    "/{grand_category_id}",
    status_code=status.HTTP_200_OK,
    response_model=GrandCategoryOutDelete,
    dependencies=[Depends(check_admin_role)])
def delete_category(grand_category_id: int, db: Session = Depends(get_db)):
    return GrandCategoryService.delete_category(db, grand_category_id)

from fastapi import APIRouter, Depends, Query, status
from app.db.database import get_db
from app.services.category_parent import ParentCategoryService
from sqlalchemy.orm import Session
from app.schemas.category_parent import ParentCategoryCreate, ParentCategoryOut, ParentCategoriesOut, ParentCategoryOutDelete, ParentCategoryUpdate
from app.core.security import check_admin_role


router = APIRouter(tags=["Parent Categories"], prefix="/category_parent")


# Get All Categories
@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=ParentCategoriesOut)
def get_all_categories(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    search: str | None = Query("", description="Search based name of parent categories"),
):
    return ParentCategoryService.get_all_categories(db, page, limit, search)


# Get Category By ID
@router.get(
    "/{parent_category_id}",
    status_code=status.HTTP_200_OK,
    response_model=ParentCategoryOut)
def get_category(parent_category_id: int, db: Session = Depends(get_db)):
    return ParentCategoryService.get_category(db, parent_category_id)


# Create New Category
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ParentCategoryOut,
    dependencies=[Depends(check_admin_role)])
def create_category(category: ParentCategoryCreate, db: Session = Depends(get_db)):
    return ParentCategoryService.create_category(db, category)


# Update Existing Category
@router.put(
    "/{parent_category_id}",
    status_code=status.HTTP_200_OK,
    response_model=ParentCategoryOut,
    dependencies=[Depends(check_admin_role)])
def update_category(parent_category_id: int, updated_category: ParentCategoryUpdate, db: Session = Depends(get_db)):
    return ParentCategoryService.update_category(db, parent_category_id, updated_category)


# Delete Category By ID
@router.delete(
    "/{parent_category_id}",
    status_code=status.HTTP_200_OK,
    response_model=ParentCategoryOutDelete,
    dependencies=[Depends(check_admin_role)])
def delete_category(parent_category_id: int, db: Session = Depends(get_db)):
    return ParentCategoryService.delete_category(db, parent_category_id)

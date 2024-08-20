from fastapi import APIRouter, Depends, Query, status
from app.db.database import get_db
from app.services.category_child import ChildCategoryService
from sqlalchemy.orm import Session
from app.schemas.category_child import ChildCategoryCreate, ChildCategoryOut, ChildCategoriesOut, ChildCategoryOutDelete, ChildCategoryUpdate
from app.core.security import check_admin_role


router = APIRouter(tags=["Child Categories"], prefix="/category_child")


# Get All Categories
@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=ChildCategoriesOut)
def get_all_categories(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    search: str | None = Query("", description="Search based name of child categories"),
):
    return ChildCategoryService.get_all_categories(db, page, limit, search)


# Get Category By ID
@router.get(
    "/{child_category_id}",
    status_code=status.HTTP_200_OK,
    response_model=ChildCategoryOut)
def get_category(child_category_id: int, db: Session = Depends(get_db)):
    return ChildCategoryService.get_category(db, child_category_id)


# Create New Category
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ChildCategoryOut,
    dependencies=[Depends(check_admin_role)])
def create_category(category: ChildCategoryCreate, db: Session = Depends(get_db)):
    return ChildCategoryService.create_category(db, category)




# Update Existing Category
@router.put(
    "/{child_category_id}",
    status_code=status.HTTP_200_OK,
    response_model=ChildCategoryOut,
    dependencies=[Depends(check_admin_role)])
def update_category(child_category_id: int, updated_category: ChildCategoryUpdate, db: Session = Depends(get_db)):
    return ChildCategoryService.update_category(db, child_category_id, updated_category)


# Delete Category By ID
@router.delete(
    "/{child_category_id}",
    status_code=status.HTTP_200_OK,
    response_model=ChildCategoryOutDelete,
    dependencies=[Depends(check_admin_role)])
def delete_category(child_category_id: int, db: Session = Depends(get_db)):
    return ChildCategoryService.delete_category(db, child_category_id)

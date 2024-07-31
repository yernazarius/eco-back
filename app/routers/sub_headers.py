from fastapi import APIRouter, Depends, Query, status
from app.db.database import get_db
from app.services.sub_headers import SubHeaderTabsService
from sqlalchemy.orm import Session
from app.schemas.sub_header_tabs import SubHeaderTabCreate, SubHeaderTabUpdate, SubHeadersOut, SubHeaderTabOut, SubHeaderTabsOutDelete
from app.core.security import check_admin_role

router = APIRouter(tags=["Sub Header Tabs"], prefix="/sub_header_tabs")

# Get All Header_tabs
@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=SubHeadersOut)
def get_all_sub_header_tabs(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    search: str | None = Query("", description="Search based name of sub_header_tabs"),
):
    return SubHeaderTabsService.get_all_sub_header_tabs(db, page, limit, search)

# Get HeaderTabs By ID
@router.get(
    "/{sub_header_tabs_id}",
    status_code=status.HTTP_200_OK,
    response_model=SubHeaderTabOut)
def get_sub_header_tab(sub_header_tabs_id: int, db: Session = Depends(get_db)):
    return SubHeaderTabsService.get_sub_header_tab(db, sub_header_tabs_id)

# Create New HeaderTabs
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=SubHeaderTabOut,
    dependencies=[Depends(check_admin_role)])
def create_sub_header_tab(sub_header_tabs: SubHeaderTabCreate, db: Session = Depends(get_db)):
    return SubHeaderTabsService.create_sub_header_tab(db, sub_header_tabs)

# Update Existing HeaderTabs
@router.put(
    "/{sub_header_tabs_id}",
    status_code=status.HTTP_200_OK,
    response_model=SubHeaderTabOut,
    dependencies=[Depends(check_admin_role)])
def update_sub_header_tab(sub_header_tabs_id: int, updated_sub_header_tabs: SubHeaderTabUpdate, db: Session = Depends(get_db)):
    return SubHeaderTabsService.update_sub_header_tab(db, sub_header_tabs_id, updated_sub_header_tabs)

# Delete HeaderTabs By ID
@router.delete(
    "/{sub_header_tabs_id}",
    status_code=status.HTTP_200_OK,
    response_model=SubHeaderTabsOutDelete,
    dependencies=[Depends(check_admin_role)])
def delete_sub_header_tab(sub_header_tabs_id: int, db: Session = Depends(get_db)):
    return SubHeaderTabsService.delete_sub_header_tab(db, sub_header_tabs_id)

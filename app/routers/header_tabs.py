from fastapi import APIRouter, Depends, Query, status
from app.db.database import get_db
from app.services.header_tabs import HeaderTabsService
from sqlalchemy.orm import Session
from app.schemas.header_tabs import HeaderTabsCreate, HeaderTabsOut, HeaderTabsOutDelete, HeaderTabsUpdate, HeaderTabOut
from app.core.security import check_admin_role

router = APIRouter(tags=["Header Tabs"], prefix="/header_tabs")

@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=HeaderTabsOut
)
def get_all_header_tabs(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    search: str | None = Query("", description="Search based name of header_tabs"),
):
    return HeaderTabsService.get_all_header_tabs(db, page, limit, search)

@router.get(
    "/{headerTabs_id}",
    status_code=status.HTTP_200_OK,
    response_model=HeaderTabOut
)
def get_header_tab(headerTabs_id: int, db: Session = Depends(get_db)):
    return HeaderTabsService.get_header_tab(db, headerTabs_id)

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=HeaderTabOut,
    dependencies=[Depends(check_admin_role)]
)
def create_header_tab(headerTabs: HeaderTabsCreate, db: Session = Depends(get_db)):
    return HeaderTabsService.create_header_tab(db, headerTabs)

@router.put(
    "/{headerTabs_id}",
    status_code=status.HTTP_200_OK,
    response_model=HeaderTabOut,
    dependencies=[Depends(check_admin_role)]
)
def update_header_tab(headerTabs_id: int, updated_headerTabs: HeaderTabsUpdate, db: Session = Depends(get_db)):
    return HeaderTabsService.update_header_tab(db, headerTabs_id, updated_headerTabs)

@router.delete(
    "/{headerTabs_id}",
    status_code=status.HTTP_200_OK,
    response_model=HeaderTabsOutDelete,
    dependencies=[Depends(check_admin_role)]
)
def delete_header_tab(headerTabs_id: int, db: Session = Depends(get_db)):
    return HeaderTabsService.delete_header_tab(db, headerTabs_id)

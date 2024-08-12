from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.header_articles import HeaderArticlesService
from app.schemas.header_articles import (
    HeaderArticleCreate,
    HeaderArticleUpdate,
    HeaderArticleOut,
    HeaderArticlesOut,
    HeaderArticlesOutDelete,
)
from app.core.security import check_admin_role

router = APIRouter(tags=["Header Articles"], prefix="/header_articles")

# Get All Header Articles
@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=HeaderArticlesOut
)
def get_all_header_articles(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    search: str | None = Query("", description="Search based on the title of header articles"),
):
    return HeaderArticlesService.get_all_header_articles(db, page, limit, search)

# Get Header Article By ID
@router.get(
    "/{header_article_id}",
    status_code=status.HTTP_200_OK,
    response_model=HeaderArticleOut
)
def get_header_article(header_article_id: int, db: Session = Depends(get_db)):
    return HeaderArticlesService.get_header_article(db, header_article_id)

# Create New Header Article
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=HeaderArticleOut,
    dependencies=[Depends(check_admin_role)]
)
def create_header_article(header_article: HeaderArticleCreate, db: Session = Depends(get_db)):
    return HeaderArticlesService.create_header_article(db, header_article)

# Update Existing Header Article
@router.put(
    "/{header_article_id}",
    status_code=status.HTTP_200_OK,
    response_model=HeaderArticleOut,
    dependencies=[Depends(check_admin_role)]
)
def update_header_article(header_article_id: int, updated_header_article: HeaderArticleUpdate, db: Session = Depends(get_db)):
    return HeaderArticlesService.update_header_article(db, header_article_id, updated_header_article)

# Delete Header Article By ID
@router.delete(
    "/{header_article_id}",
    status_code=status.HTTP_200_OK,
    response_model=HeaderArticlesOutDelete,
    dependencies=[Depends(check_admin_role)]
)
def delete_header_article(header_article_id: int, db: Session = Depends(get_db)):
    return HeaderArticlesService.delete_header_article(db, header_article_id)

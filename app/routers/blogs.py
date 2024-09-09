# app/routers/blogs.py
from fastapi import APIRouter, Depends, Query, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.blogs import BlogService
from app.schemas.blogs import BlogOut, BlogsOut, BlogUpdate
from app.core.security import check_admin_role

router = APIRouter(tags=["Blogs"], prefix="/blogs")

# Get All Blogs
@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=BlogsOut)
def get_all_blogs(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    search: str | None = Query("", description="Search based on title of blogs"),
):
    return BlogService.get_all_blogs(db, page, limit, search)


# Get Blog By ID
@router.get(
    "/{blog_id}",
    status_code=status.HTTP_200_OK,
    response_model=BlogOut)
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    return BlogService.get_blog(db, blog_id)


# Create New Blog with Image Upload
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=BlogOut,
    dependencies=[Depends(check_admin_role)])
async def create_blog(
    title: str = Form(...),
    text: str = Form(...),
    image: str = Form(...),
    db: Session = Depends(get_db)
):
    blog_data = {"title": title, "text": text, "image": None}
    return await BlogService.create_blog(db, blog_data, image)


# Update Existing Blog with Image Upload
@router.put(
    "/{blog_id}",
    status_code=status.HTTP_200_OK,
    response_model=BlogOut,
    dependencies=[Depends(check_admin_role)])
async def update_blog(
    blog_id: int,
    title: str = Form(None),
    text: str = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    blog_data = {"title": title, "text": text, "image": None}
    updated_blog = BlogUpdate(**blog_data)
    return await BlogService.update_blog(db, blog_id, updated_blog, image)


# Delete Blog By ID
@router.delete(
    "/{blog_id}",
    status_code=status.HTTP_200_OK,
    response_model=BlogOut,
    dependencies=[Depends(check_admin_role)])
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    return BlogService.delete_blog(db, blog_id)

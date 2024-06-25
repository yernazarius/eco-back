# app/services/blogs.py
import os
import shutil
from sqlalchemy.orm import Session
from fastapi import UploadFile
from app.models.models import Blog
from app.schemas.blogs import BlogCreate, BlogUpdate
from app.utils.responses import ResponseHandler

class BlogService:
    @staticmethod
    def get_all_blogs(db: Session, page: int, limit: int, search: str = ""):
        blogs = db.query(Blog).order_by(Blog.id.asc()).filter(
            Blog.title.contains(search)).limit(limit).offset((page - 1) * limit).all()
        return {"message": f"Page {page} with {limit} blogs", "data": blogs}

    @staticmethod
    def get_blog(db: Session, blog_id: int):
        blog = db.query(Blog).filter(Blog.id == blog_id).first()
        if not blog:
            ResponseHandler.not_found_error("Blog", blog_id)
        return ResponseHandler.get_single_success(blog.title, blog_id, blog)

    @staticmethod
    async def create_blog(db: Session, blog_data: dict, image: UploadFile):
        if image:
            image_path = await BlogService.save_file(image, "blogs")
            blog_data["image"] = image_path
        db_blog = Blog(**blog_data)
        db.add(db_blog)
        db.commit()
        db.refresh(db_blog)
        return ResponseHandler.create_success(db_blog.title, db_blog.id, db_blog)

    @staticmethod
    async def update_blog(db: Session, blog_id: int, updated_blog: BlogUpdate, image: UploadFile):
        db_blog = db.query(Blog).filter(Blog.id == blog_id).first()
        if not db_blog:
            ResponseHandler.not_found_error("Blog", blog_id)

        if image:
            image_path = await BlogService.save_file(image, "blogs")
            updated_blog.image = image_path

        for key, value in updated_blog.model_dump().items():
            setattr(db_blog, key, value)

        db.commit()
        db.refresh(db_blog)
        return ResponseHandler.update_success(db_blog.title, db_blog.id, db_blog)

    @staticmethod
    def delete_blog(db: Session, blog_id: int):
        db_blog = db.query(Blog).filter(Blog.id == blog_id).first()
        if not db_blog:
            ResponseHandler.not_found_error("Blog", blog_id)
        db.delete(db_blog)
        db.commit()
        return ResponseHandler.delete_success(db_blog.title, db_blog.id, db_blog)

    @staticmethod
    async def save_file(file: UploadFile, folder: str) -> str:
        file_location = f"media/{folder}"
        if not os.path.exists(file_location):
            os.makedirs(file_location)
        file_path = f"{file_location}/{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return file_path

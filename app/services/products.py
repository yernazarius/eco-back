# app/services/products.py
import os
from sqlalchemy.orm import Session
from app.models.models import Product, Category
from app.schemas.products import ProductCreate, ProductUpdate
from app.utils.responses import ResponseHandler
from fastapi import UploadFile
from typing import List
import shutil


class ProductService:
    @staticmethod
    def get_all_products(db: Session, page: int, limit: int, search: str = ""):
        products = db.query(Product).order_by(Product.id.asc()).filter(
            Product.title.contains(search)).limit(limit).offset((page - 1) * limit).all()
        return {"message": f"Page {page} with {limit} products", "data": products}

    @staticmethod
    def get_product(db: Session, product_id: int):
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            ResponseHandler.not_found_error("Product", product_id)
        return ResponseHandler.get_single_success(product.title, product_id, product)

    @staticmethod
    async def create_product(db: Session, product: ProductCreate):
        category_exists = db.query(Category).filter(Category.id == product.category_id).first()
        if not category_exists:
            ResponseHandler.not_found_error("Category", product.category_id)

        thumbnail_path = None
        if product.thumbnail:
            thumbnail_path = await ProductService.save_file(product.thumbnail, "thumbnails")

        image_paths = []
        for image in product.images:
            path = await ProductService.save_file(image, "images")
            image_paths.append(path)

        db_product = Product(
            title=product.title,
            description=product.description,
            price=product.price,
            discount_percentage=product.discount_percentage,
            rating=product.rating,
            stock=product.stock,
            brand=product.brand,
            category_id=product.category_id,
            thumbnail=thumbnail_path,
            images=image_paths,
            is_published=True
        )

        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return ResponseHandler.create_success(db_product.title, db_product.id, db_product)

    @staticmethod
    async def save_file(file: UploadFile, folder: str) -> str:
        file_location = f"media/{folder}/{file.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return file_location

    @staticmethod
    def update_product(db: Session, product_id: int, updated_product: ProductUpdate):
        db_product = db.query(Product).filter(Product.id == product_id).first()
        if not db_product:
            ResponseHandler.not_found_error("Product", product_id)

        for key, value in updated_product.dict().items():
            setattr(db_product, key, value)

        db.commit()
        db.refresh(db_product)
        return ResponseHandler.update_success(db_product.title, db_product.id, db_product)

    @staticmethod
    def delete_product(db: Session, product_id: int):
        db_product = db.query(Product).filter(Product.id == product_id).first()
        if not db_product:
            ResponseHandler.not_found_error("Product", product_id)
        db.delete(db_product)
        db.commit()
        return ResponseHandler.delete_success(db_product.title, db_product.id, db_product)

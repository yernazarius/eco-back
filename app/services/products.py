# app/services/products.py
import os
from sqlalchemy.orm import Session
from app.models.models import Product, ChildCategory, Brand
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
        category_exists = db.query(ChildCategory).filter(ChildCategory.id == product.child_category_id).first()
        if not category_exists:
            return ResponseHandler.not_found_error("Category", product.child_category_id)
        
        brand_exists = db.query(Brand).filter(Brand.id == product.brands_id).first()
        if not brand_exists:
            return ResponseHandler.not_found_error("Brand", product.brands_id)

        # Convert ProductCreate to Product SQLAlchemy model instance
        db_product = Product(
            title=product.title,
            description=product.description,
            price=product.price,
            discount_percentage=product.discount_percentage,
            rating=product.rating,
            stock=product.stock,
            brands_id=product.brands_id,
            thumbnail=product.thumbnail,
            images=product.images,
            is_published=product.is_published,
            favourite=product.favourite,
            recomended=product.recomended,
            child_category_id=product.child_category_id,
        )

        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return ResponseHandler.create_success(db_product.title, db_product.id, db_product)

    

    @staticmethod
    def update_product(db: Session, product_id: int, updated_product: ProductUpdate):
        db_product = db.query(Product).filter(Product.id == product_id).first()
        if not db_product:
            ResponseHandler.not_found_error("Product", product_id)

        for key, value in updated_product.dict(exclude_unset=True).items():
            if value is not None:
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

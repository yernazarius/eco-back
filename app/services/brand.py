from sqlalchemy.orm import Session
from app.models.models import Brand
from app.schemas.brand import BrandCreate, BrandUpdate
from app.utils.responses import ResponseHandler


class BrandService:
    @staticmethod
    def get_all_brands(db: Session, page: int, limit: int, search: str = ""):
        categories = db.query(Brand).order_by(Brand.id.asc()).filter(
            Brand.name.contains(search)).limit(limit).offset((page - 1) * limit).all()
        return {"message": f"Page {page} with {limit} brands", "data": categories}

    @staticmethod
    def get_brand(db: Session, category_id: int):
        category = db.query(Brand).filter(Brand.id == category_id).first()
        if not category:
            ResponseHandler.not_found_error("Brand", category_id)
        return ResponseHandler.get_single_success(category.name, category_id, category)

    @staticmethod
    def create_brand(db: Session, category: BrandCreate):
        category_dict = category.dict()
        db_category = Brand(**category_dict)
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return ResponseHandler.create_success(db_category.name, db_category.id, db_category)

    @staticmethod
    def update_brand(db: Session, category_id: int, updated_category: BrandUpdate):
        db_category = db.query(Brand).filter(Brand.id == category_id).first()
        if not db_category:
            ResponseHandler.not_found_error("Category", category_id)

        for key, value in updated_category.model_dump().items():
            setattr(db_category, key, value)

        db.commit()
        db.refresh(db_category)
        return ResponseHandler.update_success(db_category.name, db_category.id, db_category)

    @staticmethod
    def delete_brand(db: Session, category_id: int):
        db_category = db.query(Brand).filter(Brand.id == category_id).first()
        if not db_category:
            ResponseHandler.not_found_error("Category", category_id)
        db.delete(db_category)
        db.commit()
        return ResponseHandler.delete_success(db_category.name, db_category.id, db_category)

from sqlalchemy.orm import Session
from app.models.models import ParentCategory
from app.schemas.category_parent import ParentCategoryCreate, ParentCategoryUpdate
from app.utils.responses import ResponseHandler


class ParentCategoryService:
    @staticmethod
    def get_all_categories(db: Session, page: int, limit: int, search: str = ""):
        categories = db.query(ParentCategory).order_by(ParentCategory.id.asc()).filter(
            ParentCategory.name.contains(search)).limit(limit).offset((page - 1) * limit).all()
        return {"message": f"Page {page} with {limit} categories", "data": categories}

    @staticmethod
    def get_category(db: Session, category_id: int):
        category = db.query(ParentCategory).filter(ParentCategory.id == category_id).first()
        if not category:
            ResponseHandler.not_found_error("Category", category_id)
        return ResponseHandler.get_single_success(category.name, category_id, category)

    @staticmethod
    def create_category(db: Session, category: ParentCategoryCreate):
        category_dict = category.dict()
        db_category = ParentCategory(**category_dict)
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return ResponseHandler.create_success(db_category.name, db_category.id, db_category)

    @staticmethod
    def update_category(db: Session, category_id: int, updated_category: ParentCategoryUpdate):
        db_category = db.query(ParentCategory).filter(ParentCategory.id == category_id).first()
        if not db_category:
            ResponseHandler.not_found_error("Category", category_id)

        for key, value in updated_category.model_dump().items():
            setattr(db_category, key, value)

        db.commit()
        db.refresh(db_category)
        return ResponseHandler.update_success(db_category.name, db_category.id, db_category)

    @staticmethod
    def delete_category(db: Session, category_id: int):
        db_category = db.query(ParentCategory).filter(ParentCategory.id == category_id).first()
        if not db_category:
            ResponseHandler.not_found_error("Category", category_id)
        db.delete(db_category)
        db.commit()
        return ResponseHandler.delete_success(db_category.name, db_category.id, db_category)

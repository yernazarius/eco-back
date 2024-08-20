from sqlalchemy.orm import Session
from app.models.models import GrandCategory
from app.schemas.category_grand import GrandCategoryBase, GrandCategoryCreate, GrandCategoryUpdate
from app.utils.responses import ResponseHandler


class GrandCategoryService:
    @staticmethod
    def get_all_categories(db: Session, page: int, limit: int, search: str = ""):
        categories = db.query(GrandCategory).order_by(GrandCategory.id.asc()).filter(
            GrandCategory.name.contains(search)).limit(limit).offset((page - 1) * limit).all()
        categories_base_list = [GrandCategoryBase(id=tab.id, name=tab.name) for tab in categories]
        return {"message": f"Page {page} with {limit} categories", "data": categories_base_list}

    @staticmethod
    def get_category(db: Session, category_id: int):
        category = db.query(GrandCategory).filter(GrandCategory.id == category_id).first()
        if not category:
            ResponseHandler.not_found_error("Category", category_id)
        return ResponseHandler.get_single_success(category.name, category_id, category)

    @staticmethod
    def create_category(db: Session, category: GrandCategoryCreate):
        category_dict = category.dict()
        db_category = GrandCategory(**category_dict)
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return ResponseHandler.create_success(db_category.name, db_category.id, db_category)

    @staticmethod
    def update_category(db: Session, category_id: int, updated_category: GrandCategoryUpdate):
        db_category = db.query(GrandCategory).filter(GrandCategory.id == category_id).first()
        if not db_category:
            ResponseHandler.not_found_error("Category", category_id)

        for key, value in updated_category.model_dump().items():
            setattr(db_category, key, value)

        db.commit()
        db.refresh(db_category)
        return ResponseHandler.update_success(db_category.name, db_category.id, db_category)

    @staticmethod
    def delete_category(db: Session, category_id: int):
        db_category = db.query(GrandCategory).filter(GrandCategory.id == category_id).first()
        if not db_category:
            ResponseHandler.not_found_error("Category", category_id)
        db.delete(db_category)
        db.commit()
        return ResponseHandler.delete_success(db_category.name, db_category.id, db_category)

from sqlalchemy.orm import Session
from app.models.models import SubHeaderTabs, HeaderTabs
from app.schemas.sub_header_tabs import SubHeaderTabCreate, SubHeaderTabUpdate
from app.utils.responses import ResponseHandler

class SubHeaderTabsService:
    @staticmethod
    def get_all_sub_header_tabs(db: Session, page: int, limit: int, search: str = ""):
        header_tabs = db.query(SubHeaderTabs).order_by(SubHeaderTabs.id.asc()).filter(
            SubHeaderTabs.name.contains(search)).limit(limit).offset((page - 1) * limit).all()
        return {"message": f"Page {page} with {limit} sub header tabs", "data": header_tabs}

    @staticmethod
    def get_sub_header_tab(db: Session, sub_header_tab_id: int):
        sub_header_tab = db.query(SubHeaderTabs).filter(SubHeaderTabs.id == sub_header_tab_id).first()
        if not sub_header_tab:
            ResponseHandler.not_found_error("SubHeaderTabs", sub_header_tab_id)
        return ResponseHandler.get_single_success(sub_header_tab.name, sub_header_tab_id, sub_header_tab)

    @staticmethod
    def create_sub_header_tab(db: Session, sub_header_tab: SubHeaderTabCreate):
        header_tab_exists = db.query(HeaderTabs).filter(HeaderTabs.id == sub_header_tab.header_tab_id).first()
        if not header_tab_exists:
            ResponseHandler.not_found_error("HeaderTabs", sub_header_tab.header_tab_id)

        sub_header_tab_dict = sub_header_tab.model_dump()
        db_sub_header_tab = SubHeaderTabs(**sub_header_tab_dict)
        db.add(db_sub_header_tab)
        db.commit()
        db.refresh(db_sub_header_tab)
        return ResponseHandler.create_success(db_sub_header_tab.name, db_sub_header_tab.id, db_sub_header_tab)

    @staticmethod
    def update_sub_header_tab(db: Session, sub_header_tab_id: int, updated_sub_header_tab: SubHeaderTabUpdate):
        db_sub_header_tab = db.query(SubHeaderTabs).filter(SubHeaderTabs.id == sub_header_tab_id).first()
        if not db_sub_header_tab:
            ResponseHandler.not_found_error("SubHeaderTabs", sub_header_tab_id)

        for key, value in updated_sub_header_tab.model_dump().items():
            setattr(db_sub_header_tab, key, value)

        db.commit()
        db.refresh(db_sub_header_tab)
        return ResponseHandler.update_success(db_sub_header_tab.name, db_sub_header_tab.id, db_sub_header_tab)

    @staticmethod
    def delete_sub_header_tab(db: Session, sub_header_tab_id: int):
        db_sub_header_tab = db.query(SubHeaderTabs).filter(SubHeaderTabs.id == sub_header_tab_id).first()
        if not db_sub_header_tab:
            ResponseHandler.not_found_error("SubHeaderTabs", sub_header_tab_id)
        db.delete(db_sub_header_tab)
        db.commit()
        return ResponseHandler.delete_success(db_sub_header_tab.name, db_sub_header_tab.id, db_sub_header_tab)

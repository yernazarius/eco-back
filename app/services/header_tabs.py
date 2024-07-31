from sqlalchemy.orm import Session
from app.models.models import HeaderTabs
from app.schemas.header_tabs import HeaderTabsCreate, HeaderTabsUpdate, HeaderTabsBase, HeaderTabOut, HeaderTabsOut, HeaderTabsDelete, HeaderTabsOutDelete
from app.utils.responses import ResponseHandler

class HeaderTabsService:
    @staticmethod
    def get_all_header_tabs(db: Session, page: int, limit: int, search: str = "") -> HeaderTabsOut:
        header_tabs = db.query(HeaderTabs).order_by(HeaderTabs.id.asc()).filter(
            HeaderTabs.name.contains(search)).limit(limit).offset((page - 1) * limit).all()
        header_tabs_base_list = [HeaderTabsBase(id=tab.id, name=tab.name) for tab in header_tabs]
        return HeaderTabsOut(message=f"Page {page} with {limit} header tabs", data=header_tabs_base_list)

    @staticmethod
    def get_header_tab(db: Session, header_tabs_id: int) -> HeaderTabOut:
        header_tab = db.query(HeaderTabs).filter(HeaderTabs.id == header_tabs_id).first()
        if not header_tab:
            ResponseHandler.not_found_error("HeaderTabs", header_tabs_id)
        return HeaderTabOut(message="HeaderTab retrieved successfully", data=HeaderTabsBase(id=header_tab.id, name=header_tab.name))

    @staticmethod
    def create_header_tab(db: Session, header_tabs: HeaderTabsCreate) -> HeaderTabOut:
        header_tabs_dict = header_tabs.dict()
        db_header_tabs = HeaderTabs(**header_tabs_dict)
        db.add(db_header_tabs)
        db.commit()
        db.refresh(db_header_tabs)
        return HeaderTabOut(message="HeaderTab created successfully", data=HeaderTabsBase(id=db_header_tabs.id, name=db_header_tabs.name))

    @staticmethod
    def update_header_tab(db: Session, header_tabs_id: int, updated_header_tabs: HeaderTabsUpdate) -> HeaderTabOut:
        db_header_tabs = db.query(HeaderTabs).filter(HeaderTabs.id == header_tabs_id).first()
        if not db_header_tabs:
            ResponseHandler.not_found_error("HeaderTabs", header_tabs_id)

        for key, value in updated_header_tabs.model_dump().items():
            setattr(db_header_tabs, key, value)

        db.commit()
        db.refresh(db_header_tabs)
        return HeaderTabOut(message="HeaderTab updated successfully", data=HeaderTabsBase(id=db_header_tabs.id, name=db_header_tabs.name))

    @staticmethod
    def delete_header_tab(db: Session, header_tabs_id: int) -> HeaderTabsOutDelete:
        db_header_tabs = db.query(HeaderTabs).filter(HeaderTabs.id == header_tabs_id).first()
        if not db_header_tabs:
            ResponseHandler.not_found_error("HeaderTabs", header_tabs_id)
        db.delete(db_header_tabs)
        db.commit()
        return HeaderTabsOutDelete(message="HeaderTab deleted successfully", data=HeaderTabsDelete(id=db_header_tabs.id, name=db_header_tabs.name))

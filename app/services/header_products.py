from sqlalchemy.orm import Session
from app.models.models import HeaderProducts, SubHeaderTabs as Category
from app.schemas.header_products import HeaderProductCreate, HeaderProductsUpdate
from app.utils.responses import ResponseHandler


class HeaderProductService:
    @staticmethod
    def get_all_header_products(db: Session, page: int, limit: int, search: str = ""):
        headerProducts = db.query(HeaderProducts).order_by(HeaderProducts.id.asc()).filter(
            HeaderProducts.title.contains(search)).limit(limit).offset((page - 1) * limit).all()
        return {"message": f"Page {page} with {limit} headerProducts", "data": headerProducts}

    @staticmethod
    def get_header_product(db: Session, headerProduct_id: int):
        headerProduct = db.query(HeaderProducts).filter(HeaderProducts.id == headerProduct_id).first()
        if not headerProduct:
            ResponseHandler.not_found_error("HeaderProduct", headerProduct_id)
        return ResponseHandler.get_single_success(headerProduct.title, headerProduct_id, headerProduct)

    @staticmethod
    def create_header_product(db: Session, headerProduct: HeaderProductCreate):
        category_exists = db.query(Category).filter(Category.id == headerProduct.sub_header_tabs_id).first()
        if not category_exists:
            ResponseHandler.not_found_error("Category", headerProduct.sub_header_tabs_id)

        headerProduct_dict = headerProduct.model_dump()
        db_headerProduct = HeaderProducts(**headerProduct_dict)
        db.add(db_headerProduct)
        db.commit()
        db.refresh(db_headerProduct)
        return ResponseHandler.create_success(db_headerProduct.title, db_headerProduct.id, db_headerProduct)

    @staticmethod
    def update_header_product(db: Session, headerProduct_id: int, updated_headerProduct: HeaderProductsUpdate):
        db_headerProduct = db.query(HeaderProducts).filter(HeaderProducts.id == headerProduct_id).first()
        if not db_headerProduct:
            ResponseHandler.not_found_error("HeaderProduct", headerProduct_id)

        for key, value in updated_headerProduct.model_dump().items():
            setattr(db_headerProduct, key, value)

        db.commit()
        db.refresh(db_headerProduct)
        return ResponseHandler.update_success(db_headerProduct.title, db_headerProduct.id, db_headerProduct)

    @staticmethod
    def delete_header_product(db: Session, headerProduct_id: int):
        db_headerProduct = db.query(HeaderProducts).filter(HeaderProducts.id == headerProduct_id).first()
        if not db_headerProduct:
            ResponseHandler.not_found_error("HeaderProduct", headerProduct_id)
        db.delete(db_headerProduct)
        db.commit()
        return ResponseHandler.delete_success(db_headerProduct.title, db_headerProduct.id, db_headerProduct)

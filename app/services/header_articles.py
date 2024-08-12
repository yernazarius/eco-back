from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.models import HeaderArticles
from app.schemas.header_articles import HeaderArticleCreate, HeaderArticleUpdate

class HeaderArticlesService:

    @staticmethod
    def get_all_header_articles(db: Session, page: int, limit: int, search: str):
        query = db.query(HeaderArticles).filter(HeaderArticles.title.ilike(f"%{search}%"))
        total_items = query.count()
        articles = query.offset((page - 1) * limit).limit(limit).all()

        return {
            "total_items": total_items,
            "page": page,
            "limit": limit,
            "articles": articles
        }

    @staticmethod
    def get_header_article(db: Session, article_id: int):
        article = db.query(HeaderArticles).filter(HeaderArticles.id == article_id).first()
        if not article:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
        return article

    @staticmethod
    def create_header_article(db: Session, article_data: HeaderArticleCreate):
        new_article = HeaderArticles(**article_data.dict())
        db.add(new_article)
        db.commit()
        db.refresh(new_article)
        return new_article

    @staticmethod
    def update_header_article(db: Session, article_id: int, updated_data: HeaderArticleUpdate):
        article = db.query(HeaderArticles).filter(HeaderArticles.id == article_id).first()
        if not article:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")

        for key, value in updated_data.dict().items():
            setattr(article, key, value)

        db.commit()
        db.refresh(article)
        return article

    @staticmethod
    def delete_header_article(db: Session, article_id: int):
        article = db.query(HeaderArticles).filter(HeaderArticles.id == article_id).first()
        if not article:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
        
        db.delete(article)
        db.commit()
        return {"message": "Article deleted successfully"}

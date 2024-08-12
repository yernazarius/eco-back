from pydantic import BaseModel
from typing import List, Union
from datetime import datetime

# Reuse existing HeaderArticleContentItem, HeaderArticleCreate, HeaderArticleUpdate

class HeaderArticleContentItem(BaseModel):
    type: str  # 'text' or 'image'
    value: str

class HeaderArticleCreate(BaseModel):
    title: str
    content: List[HeaderArticleContentItem]
    sub_header_tabs_id: int

class HeaderArticleUpdate(BaseModel):
    title: str
    content: List[HeaderArticleContentItem]

# Schema for the individual article output
class HeaderArticleOut(BaseModel):
    id: int
    title: str
    content: List[HeaderArticleContentItem]
    sub_header_tabs_id: int
    created_at: datetime

    class Config:
        orm_mode = True  # Enables ORM compatibility for SQLAlchemy models

# Schema for outputting multiple articles (with pagination info)
class HeaderArticlesOut(BaseModel):
    total_items: int
    page: int
    limit: int
    articles: List[HeaderArticleOut]

# Schema for deletion response
class HeaderArticlesOutDelete(BaseModel):
    message: str

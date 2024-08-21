from typing import List, Optional
from pydantic import BaseModel, Field
from app.schemas.category_parent import ParentCategoryProduct

# Base schema for ChildCategory
class ChildCategoryBase(BaseModel):
    id: int
    name: str
    parent_category_id: int

    class Config:
        orm_mode = True

class ChildCategoryProduct(BaseModel):
    id: int
    name: str
    parent_category_id: int
    parent_category: ParentCategoryProduct


# Schema for creating a new ChildCategory
class ChildCategoryCreate(BaseModel):
    name: str
    parent_category_id: int

# Schema for updating an existing ChildCategory
class ChildCategoryUpdate(BaseModel):
    name: Optional[str] = None
    parent_category_id: Optional[int] = None

# Output schema for a single ChildCategory
class ChildCategoryOut(BaseModel):
    message: str
    data: ChildCategoryBase

# Output schema for a list of ChildCategories
class ChildCategoriesOut(BaseModel):
    message: str
    data: List[ChildCategoryBase]

# Schema for delete operation
class ChildCategoryDelete(BaseModel):
    id: int
    name: str

class ChildCategoryOutDelete(BaseModel):
    message: str
    data: ChildCategoryDelete

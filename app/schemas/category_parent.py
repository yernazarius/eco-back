from typing import List, Optional
from pydantic import BaseModel, Field
from app.schemas.category_grand import GrandCategoryBase

# Base schema for ParentCategory
class ParentCategoryBase(BaseModel):
    id: int
    name: str
    image_path: Optional[str] = None
    grand_category_id: int

    class Config:
        orm_mode = True


class ParentCategoryProduct(BaseModel):
    name: str
    image_path: Optional[str] = None
    grand_category_id: int
    grand_category: GrandCategoryBase


# Schema for creating a new ParentCategory
class ParentCategoryCreate(BaseModel):
    name: str
    image_path: Optional[str] = None
    grand_category_id: int

# Schema for updating an existing ParentCategory
class ParentCategoryUpdate(BaseModel):
    name: Optional[str] = None
    image_path: Optional[str] = None
    grand_category_id: Optional[int] = None

# Output schema for a single ParentCategory
class ParentCategoryOut(BaseModel):
    message: str
    data: ParentCategoryBase

# Output schema for a list of ParentCategories
class ParentCategoriesOut(BaseModel):
    message: str
    data: List[ParentCategoryBase]

# Schema for delete operation
class ParentCategoryDelete(BaseModel):
    id: int
    name: str

class ParentCategoryOutDelete(BaseModel):
    message: str
    data: ParentCategoryDelete

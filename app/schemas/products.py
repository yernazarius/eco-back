from fastapi import UploadFile
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import List, Optional
from app.schemas.category_child import ChildCategoryBase

class BaseConfig:
    from_attributes = True
# Base schema for Product
class ProductBase(BaseModel):
    id: int
    title: str
    description: str
    price: int
    discount_percentage: float
    rating: float
    stock: int
    brand: str
    thumbnail: str
    images: List[str]
    is_published: bool = Field(default=True)
    # created_at: datetime
    favourite: bool
    recomended: bool
    child_category_id: int
    child_category: ChildCategoryBase

    class Config:
        orm_mode = True

# Schema for creating a new Product
class ProductCreate(BaseModel):
    title: str
    description: str
    price: int
    discount_percentage: float
    rating: float
    stock: int
    brand: str
    thumbnail: str
    images: List[str]
    is_published: Optional[bool] = Field(default=True)
    favourite: bool
    recomended: bool
    child_category_id: int
    
    class Config:
        orm_mode = True

# Schema for updating an existing Product
class ProductUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    discount_percentage: Optional[float] = None
    rating: Optional[float] = None
    stock: Optional[int] = None
    brand: Optional[str] = None
    thumbnail: Optional[str] = None
    images: Optional[List[str]] = None
    is_published: Optional[bool] = None
    favourite: Optional[bool] = None
    recomended: Optional[bool] = None
    child_category_id: Optional[int] = None

# Output schema for a single Product
class ProductOut(BaseModel):
    message: str
    data: ProductBase

# Output schema for a list of Products
class ProductsOut(BaseModel):
    message: str
    data: List[ProductBase]

# Schema for delete operation
class ProductDelete(BaseModel):
    id: int
    title: str

class ProductOutDelete(BaseModel):
    message: str
    data: ProductDelete

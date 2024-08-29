from fastapi import UploadFile
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import List, Optional
from app.schemas.category_child import ChildCategoryProduct, ChildCategoryBase
from app.schemas.brand import BrandProduct

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
    brands_id: int
    brand: BrandProduct
    thumbnail: str
    images: List[str]
    is_published: bool = Field(default=True)
    # created_at: datetime
    favourite: bool
    recomended: bool
    child_category_id: int
    child_category: ChildCategoryProduct

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
    brands_id: int
    thumbnail: str
    images: List[str]
    is_published: Optional[bool] = Field(default=True)
    favourite: bool
    recomended: bool
    child_category_id: int

    @validator('price')
    def validate_price(cls, v):
        if v is None or v <= 0:
            raise ValueError("Price must be a positive integer")
        return v
    
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
    brands_id: Optional[int] = None
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

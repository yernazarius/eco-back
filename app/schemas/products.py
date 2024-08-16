from fastapi import UploadFile
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import List, Optional
from app.schemas.categories import CategoryBase


# Base Models
class BaseConfig:
    from_attributes = True


class ProductBase(BaseModel):
    id: int
    title: str
    description: Optional[str]
    price: int
    discount_percentage: float
    rating: float
    stock: int
    brand: str
    thumbnail: str
    images: List[str]
    is_published: bool
    created_at: datetime
    favourite: bool
    recomended: bool
    category_id: int
    category: CategoryBase

    class Config(BaseConfig):
        pass


# Create Product
class ProductCreate(BaseModel):
    title: str
    description: Optional[str]
    price: int
    discount_percentage: float
    rating: float
    stock: int
    brand: str
    category_id: int
    favourite: bool
    recomended: bool
    thumbnail: Optional[UploadFile] = Field(None, description="Thumbnail image")
    images: List[UploadFile] = Field([], description="List of images")

    @validator("discount_percentage")
    def validate_discount_percentage(cls, v):
        if v < 0 or v > 100:
            raise ValueError("discount_percentage must be between 0 and 100")
        return v

    class Config(BaseConfig):
        pass


# Update Product
class ProductUpdate(ProductCreate):
    pass


# Get Products
class ProductOut(BaseModel):
    message: str
    data: ProductBase

    class Config(BaseConfig):
        pass


class ProductsOut(BaseModel):
    message: str
    data: List[ProductBase]

    class Config(BaseConfig):
        pass


# Delete Product
class ProductDelete(ProductBase):
    pass


class ProductOutDelete(BaseModel):
    message: str
    data: ProductDelete

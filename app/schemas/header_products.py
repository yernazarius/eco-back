from pydantic import BaseModel, validator
from datetime import datetime
from typing import List, Optional, ClassVar
from app.schemas.sub_header_tabs import SubHeaderTabBase


# Base Models
class BaseConfig:
    from_attributes = True


class HeaderProductsBase(BaseModel):
    id: int
    title: str
    description: Optional[str]
    price: int

    @validator("discount_percentage", pre=True)
    def validate_discount_percentage(cls, v):
        if v < 0 or v > 100:
            raise ValueError("discount_percentage must be between 0 and 100")
        return v

    discount_percentage: float
    rating: float
    stock: int
    brand: str
    thumbnail: str
    images: List[str]
    is_published: bool
    created_at: datetime
    category_id: int
    category: SubHeaderTabBase

    class Config(BaseConfig):
        pass


# Create HeaderProducts
class HeaderProductsCreate(HeaderProductsBase):
    id: ClassVar[int]
    category: ClassVar[SubHeaderTabBase]

    class Config(BaseConfig):
        pass


# Update HeaderProducts
class HeaderProductsUpdate(HeaderProductsCreate):
    pass


# Get HeaderProductss
class HeaderProductsOut(BaseModel):
    message: str
    data: HeaderProductsBase

    class Config(BaseConfig):
        pass


class HeaderProductssOut(BaseModel):
    message: str
    data: List[HeaderProductsBase]

    class Config(BaseConfig):
        pass


# Delete HeaderProducts
class HeaderProductsDelete(HeaderProductsBase):
    category: ClassVar[SubHeaderTabBase]


class HeaderProductsOutDelete(BaseModel):
    message: str
    data: HeaderProductsDelete

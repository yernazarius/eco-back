from typing import List, Optional
from pydantic import BaseModel, Field

class BaseConfig:
    from_attributes = True

# Base schema for Brand
class BrandBase(BaseModel):
    id: int
    name: str

    class Config(BaseConfig):
        pass



class BrandProduct(BaseModel):
    id: int
    name: str


# Schema for creating a new Brand
class BrandCreate(BaseModel):
    name: str

# Schema for updating an existing Brand
class BrandUpdate(BaseModel):
    name: Optional[str] = None

# Output schema for a single Brand
class BrandOut(BaseModel):
    message: str
    data: BrandBase

# Output schema for a list of Brand
class BrandsOut(BaseModel):
    message: str
    data: List[BrandBase]

# Schema for delete operation
class BrandDelete(BaseModel):
    id: int
    name: str

class BrandOutDelete(BaseModel):
    message: str
    data: BrandDelete

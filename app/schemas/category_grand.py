from typing import List
from pydantic import BaseModel, Field


class GrandCategoryBase(BaseModel):
    id: int
    name: str


class GrandCategoryCreate(BaseModel):
    name: str


class GrandCategoryUpdate(BaseModel):
    name: str


class GrandCategoryOut(BaseModel):
    message: str
    data: GrandCategoryBase


class GrandCategoriesOut(BaseModel):
    message: str
    data: List[GrandCategoryBase]


class GrandCategoryDelete(BaseModel):
    id: int
    name: str


class GrandCategoryOutDelete(BaseModel):
    message: str
    data: GrandCategoryDelete

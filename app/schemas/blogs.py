# app/schemas/blogs.py
from typing import List
from pydantic import BaseModel

class BlogBase(BaseModel):
    id: int
    title: str
    text: str
    image: str | None

    class Config:
        orm_mode = True

class BlogCreate(BaseModel):
    title: str
    text: str
    image: str | None  # Make image optional

class BlogUpdate(BaseModel):
    title: str | None
    text: str | None
    image: str | None

class BlogOut(BaseModel):
    message: str
    data: BlogBase

class BlogsOut(BaseModel):
    message: str
    data: List[BlogBase]

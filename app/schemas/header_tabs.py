from typing import List
from pydantic import BaseModel, Field


class HeaderTabsBase(BaseModel):
    id: int
    name: str


class HeaderTabsCreate(BaseModel):
    name: str


class HeaderTabsUpdate(BaseModel):
    name: str


class HeaderTabOut(BaseModel):
    message: str
    data: HeaderTabsBase


class HeaderTabsOut(BaseModel):
    message: str
    data: List[HeaderTabsBase]


class HeaderTabsDelete(BaseModel):
    id: int
    name: str


class HeaderTabsOutDelete(BaseModel):
    message: str
    data: HeaderTabsDelete

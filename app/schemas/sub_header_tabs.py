from typing import List
from pydantic import BaseModel, Field
from app.schemas.header_tabs import HeaderTabsBase

class SubHeaderTabBase(BaseModel):
    id: int
    name: str
    header_tab_id: int  # Adding the header_tab_id field
    # header_tab: HeaderTabsBase

class SubHeaderTabCreate(BaseModel):
    name: str
    header_tab_id: int  # Adding the header_tab_id field

class SubHeaderTabUpdate(BaseModel):
    name: str
    header_tab_id: int  # Adding the header_tab_id field

class SubHeaderTabOut(BaseModel):
    message: str
    data: SubHeaderTabBase

class SubHeadersOut(BaseModel):
    message: str
    data: List[SubHeaderTabBase]

class SubHeaderTabsDelete(BaseModel):
    id: int
    name: str

class SubHeaderTabsOutDelete(BaseModel):
    message: str
    data: SubHeaderTabsDelete

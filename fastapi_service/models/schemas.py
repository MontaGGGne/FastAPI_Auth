from uuid import UUID
from fastapi import UploadFile
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from models.core import Item


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreateUpdate(ItemBase):
    filename: str
    item_data: UploadFile
    id: Optional[int] = None


class Item(ItemBase):
    id: int
    owner_id: int
    s3_path: str
    
    class Config:
        orm_mode = True


class LiteItem(ItemBase):
    id: int
    s3_path: str


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str
    

UserAuth = UserCreate


class LiteUser(UserBase):
    id: int


class User(UserBase):
    id: int
    is_active: bool
    s3_folder_id: UUID
    items: List[Item] = []
    
    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
from uuid import UUID
from fastapi import UploadFile
from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any
from models.core import Item


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class Item(ItemBase):
    id: int
    owner_id: int
    s3_path: str
    
    class Config:
        orm_mode = True


class LiteItem(ItemBase):
    id: int
    s3_path: str


class ItemPredict(ItemBase):
    id: int
    predict: dict


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str
    

UserAuth = UserCreate


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    name: Optional[str] = None
    surname: Optional[str] = None


class User(UserBase):
    id: int
    is_active: bool
    s3_folder_id: UUID
    items: List[Item] = []
    
    class Config:
        orm_mode = True


class LiteUser(UserBase):
    id: int
    name: Optional[str] = None
    surname: Optional[str] = None


class Token(BaseModel):
    access_token: str
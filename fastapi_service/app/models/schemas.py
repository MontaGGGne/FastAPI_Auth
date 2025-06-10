from uuid import UUID
from pydantic import BaseModel, EmailStr
from typing import List, Optional

from app.models.core import Item


# Базовые классы

class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class UserBase(BaseModel):
    email: EmailStr


# Классы форм

class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    name: Optional[str] = None
    surname: Optional[str] = None


UserAuth = UserCreate


# Классы представлений

class Item(ItemBase):
    id: int
    owner_id: int
    s3_path: str
    
    class Config:
        from_attributes = True


class LiteItem(ItemBase):
    id: int
    s3_path: str


class ItemPredict(ItemBase):
    id: int
    predict: dict


class User(UserBase):
    id: int
    is_active: bool
    s3_folder_id: UUID
    items: List[Item] = []
    
    class Config:
        from_attributes = True


class LiteUser(UserBase):
    id: int
    name: Optional[str] = None
    surname: Optional[str] = None


class Token(BaseModel):
    access_token: str
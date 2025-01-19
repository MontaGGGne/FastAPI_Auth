from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED

from models.core import User, Token
from models.schemas import UserCreate, UserUpdate, LiteUser
from secure import pwd_context


def register(db: Session, user_data: UserCreate):
    if db.scalar(select(User).where(User.email == user_data.email)):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="User with this email already exists!"
        )
    user = User(email=user_data.email)
    user.hashed_password = pwd_context.hash(user_data.password)
    user.s3_folder_id = uuid4()
    db.add(user)
    db.commit()
    return LiteUser(
        id=user.id,
        email=user.email,
        name=user.name,
        surname=user.surname
    )

def update(access_token: str, db: Session, user_update: UserUpdate):
    token = db.scalar(select(Token).where(Token.access_token == access_token))
    if token:
        user = db.scalar(select(User).where(User.id == token.user.id))
        if not user:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        if user_update.password:
            user.hashed_password = pwd_context.hash(user_update.password)
        for key, value in user_update.model_dump().items():
            setattr(user, key, value) if value else None
        db.commit()
        db.refresh(user)
        return LiteUser(
            id=user.id,
            email=user.email,
            name=user.name,
            surname=user.surname
        )
    else:
        raise HTTPException(
            status_code = HTTP_401_UNAUTHORIZED,
            detail = "UNAUTHORIZED"
        )

def delete_user_by_token(access_token: str, db: Session):
    token = db.scalar(select(Token).where(Token.access_token == access_token))
    if token:
        user = db.scalar(select(User).where(User.id == token.user.id))
        if not user:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        db.delete(user)
        db.commit()
        return {"ok": True}
    else:
        raise HTTPException(
            status_code = HTTP_401_UNAUTHORIZED,
            detail = "UNAUTHORIZED"
        )
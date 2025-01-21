from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED

from app.models.core import Token, User
from app.models.schemas import LiteUser


def all_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def user_by_token(access_token: str, db: Session):
    token = db.scalar(select(Token).where(Token.access_token == access_token))
    if token:
        return LiteUser(
            id=token.user.id,
            email=token.user.email,
            name=token.user.name,
            surname=token.user.surname
        )
    else:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail = "UNAUTHORIZED"
        )
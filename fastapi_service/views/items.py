from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED

from models.core import Item, Token


def all_items(access_token: str, db: Session, skip: int = 0, limit: int = 100):
    token = db.scalar(select(Token).where(Token.access_token == access_token))
    if token:
        return db.query(Item).where(Item.owner_id == token.user.id).offset(skip).limit(limit).all()
    else:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail = "UNAUTHORIZED"
        )

def item_by_id(access_token: str, item_id: str, db: Session):
    token = db.scalar(select(Token).where(Token.access_token == access_token))
    if token:
        return db.scalar(select(Item).where(Item.owner_id == token.user.id).where(Item.id == item_id))
    else:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail = "UNAUTHORIZED"
        )
    
from uuid import uuid4
from fastapi import HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

from typing import Optional, Dict, Any

from models.core import Item, Token
from models.schemas import LiteItem

from additional_methods.upload_file import upload_json
from additional_methods.get_env import *


async def item_create(access_token: str,
                       db: Session,
                       item_data: UploadFile,
                       title: str,
                       description: Optional[str] = None):
    token = db.scalar(select(Token).where(Token.access_token == access_token))
    if token:
        uuid_filename = uuid4()
        s3_full_path = f"{CORE_FOLDER}/users/{str(token.user.s3_folder_id)}/{str(uuid_filename)}.json"
        await upload_json(item_data, s3_full_path)
        item = Item(title=title,
                    description=description,
                    s3_path=s3_full_path)
        item.owner_id = token.user.id
        db.add(item)
        db.commit()
        return LiteItem(id=item.id,
                        title=item.title,
                        description=item.description,
                        s3_path=item.s3_path)
    else:
        raise HTTPException(
            status_code = HTTP_401_UNAUTHORIZED,
            detail = "UNAUTHORIZED"
        )

async def item_update(access_token: str,
                       db: Session,
                       id: int,
                       item_data: Optional[UploadFile] = None,
                       title: Optional[str] = None,
                       description: Optional[str] = None):
    token = db.scalar(select(Token).where(Token.access_token == access_token))
    if token:
        cur_item = db.scalar(select(Item).where(Item.id == id))
        if not cur_item:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail="Item not found"
            )
        item_fields: Dict[str, Any] = {
            "title": title,
            "description": description,
        }
        if item_data is not None:
            await upload_json(item_data, cur_item.s3_path)
        for key, value in item_fields.items():
            setattr(cur_item, key, value) if value else None
        db.commit()
        db.refresh(cur_item)
        return LiteItem(id=cur_item.id,
                        title=cur_item.title,
                        description=cur_item.description,
                        s3_path=cur_item.s3_path)
    else:
        raise HTTPException(
            status_code = HTTP_401_UNAUTHORIZED,
            detail = "UNAUTHORIZED"
        )

def delete_item_by_id(access_token: str, item_id: str, db: Session):
    token = db.scalar(select(Token).where(Token.access_token == access_token))
    if token:
        cur_item = db.scalar(select(Item).where(Item.id == item_id))
        if not cur_item:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail="Item not found"
            )
        db.delete(cur_item)
        db.commit()
        return {"ok": True}
    else:
        raise HTTPException(
            status_code = HTTP_401_UNAUTHORIZED,
            detail = "UNAUTHORIZED"
        )

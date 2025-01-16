from fastapi import HTTPException, UploadFile, File
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED

from models.core import Item, Token
from models.schemas import ItemCreateUpdate, LiteItem

from additional_methods.upload_file import upload_json


def item_add_update(access_token: str, db: Session, item_fields: ItemCreateUpdate,
                    item_data):
    token = db.scalar(select(Token).where(Token.access_token == access_token))
    if token:
        s3_path = upload_json(item_data, str(token.user.s3_folder_id),
                              item_fields.filename)
        item = Item(title=item_fields.title,
                    description=item_fields.description,
                    s3_path=s3_path)
        item.owner_id = token.user.id
        db.add(item)
        db.commit()
        return LiteItem(id=item.id,
                        title=item.title,
                        description=item.description,
                        s3_path=item.s3_path)
    else:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail = "UNAUTHORIZED"
        )
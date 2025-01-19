import traceback
from fastapi import HTTPException
import requests
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from fastapi.responses import StreamingResponse

import io
import json

from models.core import Item, Token

from s3.s3_methods import s3_get_signature
from s3.s3_conn import boto3_conn

from models.schemas import ItemPredict

from additional_methods.get_env import *


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

def item_by_id_download(access_token: str, item_id: int, db: Session):
    token = db.scalar(select(Token).where(Token.access_token == access_token))
    if token:
        cur_item = db.scalar(select(Item).where(Item.id == item_id))
        if not cur_item:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail="Item not found"
            )
        get_signature = s3_get_signature(s3_session=boto3_conn(),
                                    bucket=BUCKET_ID,
                                    key=cur_item.s3_path)
        get_resp = requests.get(get_signature)
        if get_resp.reason != 'OK':
            raise HTTPException(
                status_code=get_resp.status_code,
                detail = "Get signature error"
            )
        file = io.BytesIO(get_resp.content)
        filename = str(cur_item.s3_path).split('/')[-1]
        headers = {"content-disposition": "attachment; filename=\"{}\"".format(filename)}
        return StreamingResponse(content=file, media_type='application/octet-stream', headers=headers)
    else:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail = "UNAUTHORIZED"
        )

def predict(access_token: str, item_id: str, db: Session, ml_model):
    token = db.scalar(select(Token).where(Token.access_token == access_token))
    if token:
        cur_item = db.scalar(select(Item).where(Item.id == item_id))
        if not cur_item:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail="Item not found"
            )
        get_signature = s3_get_signature(s3_session=boto3_conn(),
                                    bucket=BUCKET_ID,
                                    key=cur_item.s3_path)
        get_resp = requests.get(get_signature)
        if get_resp.reason != 'OK':
            raise HTTPException(
                status_code=get_resp.status_code,
                detail = "Get signature error"
            )
        file_content = get_resp.content
        json_data = file_content.decode('utf8').replace("'", '"')
        data_obj = json.loads(json_data)
        print(f"data_obj: {data_obj}")
        response_model: dict = {}
        if ml_model is None:
            raise HTTPException(
                status_code = HTTP_500_INTERNAL_SERVER_ERROR,
                detail = f"None model"
            )
        try:
            response_model = ml_model(data_obj)
        except Exception as e:
            raise HTTPException(
                status_code = HTTP_500_INTERNAL_SERVER_ERROR,
                detail = f"Get predict from model error: {traceback.format_exc()}"
            )
        return ItemPredict(
            id=cur_item.id,
            title=cur_item.title,
            description=cur_item.description,
            predict=response_model
        )
    else:
        raise HTTPException(
            status_code = HTTP_401_UNAUTHORIZED,
            detail = "UNAUTHORIZED"
        )
    
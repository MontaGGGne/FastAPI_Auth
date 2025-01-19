from fastapi import APIRouter, UploadFile, File, Body, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session
from fastapi import HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from typing import Annotated, List, Optional

from views.items import all_items, item_by_id, item_by_id_download, predict

from models import schemas
from models.database import get_db

from controllers.items import item_create, item_update, delete_item_by_id
from secure import apikey_scheme

from additional_methods.get_env import *

from ml.model import load_autoencoder_model


ml_model = None
router = APIRouter()

@router.on_event("startup")
async def startup_event():
    try:
        global ml_model
        ml_model = load_autoencoder_model()
    except:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Error load autoencoder model"
        )

@router.get("/", response_model=List[schemas.Item])
def get_all_items(access_token: Annotated[str, Depends(apikey_scheme)],
                  skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return all_items(access_token=access_token, db=db, skip=skip, limit=limit)

@router.get("/{item_id}", response_model=schemas.LiteItem)
def get_item(item_id: int, access_token: Annotated[str, Depends(apikey_scheme)],
             db: Session = Depends(get_db)):
    return item_by_id(item_id=item_id, access_token=access_token, db=db)

@router.get("/{item_id}/download",
            responses = {
                200: {
                    "content": {"application/octet-stream": {}}
                }
            },
            response_class=Response)
def download_item_file(item_id: int, access_token: Annotated[str, Depends(apikey_scheme)],
             db: Session = Depends(get_db)):
    return item_by_id_download(item_id=item_id, access_token=access_token, db=db)

@router.get("/{item_id}/predict")
async def get_predict(item_id: int, access_token: Annotated[str, Depends(apikey_scheme)],
             db: Session = Depends(get_db)):
    return predict(item_id=item_id, access_token=access_token, db=db, ml_model=ml_model)

@router.post("", response_model=schemas.LiteItem, status_code=201)
async def create_item(access_token: Annotated[str, Depends(apikey_scheme)],
                      title: str,
                      description: Optional[str] = None,
                      item_data: UploadFile = File(...),
                      db: Session = Depends(get_db)):
    return await item_create(access_token, db=db,
                                    title=title,
                                    description=description,
                                    item_data=item_data)

@router.put("/{item_id}", response_model=schemas.LiteItem, status_code=201)
async def update_item(access_token: Annotated[str, Depends(apikey_scheme)],
                item_id: int,
                title: Optional[str] = None,
                description: Optional[str] = None,
                item_data: Optional[UploadFile] = None,
                db: Session = Depends(get_db)):
    return await item_update(access_token, db=db,
                       id=item_id,
                       title=title,
                       description=description,
                       item_data=item_data)

@router.delete("/{item_id}")
def delete_item(item_id: int, access_token: Annotated[str, Depends(apikey_scheme)],
             db: Session = Depends(get_db)):
    return delete_item_by_id(item_id=item_id, access_token=access_token, db=db)
    

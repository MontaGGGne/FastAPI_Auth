from fastapi import APIRouter, UploadFile, File, Body, Depends
from sqlalchemy.orm import Session

from typing import Annotated, List

from views.items import all_items, item_by_id

from models import schemas
from models.database import get_db

from controllers.items import item_add_update
from secure import apikey_scheme


router = APIRouter()

@router.get("/", response_model=List[schemas.Item])
def get_all_items(access_token: Annotated[str, Depends(apikey_scheme)],
                  skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return all_items(access_token=access_token, db=db, skip=skip, limit=limit)

@router.get("/{item_id}")
def get_item(item_id: int, access_token: Annotated[str, Depends(apikey_scheme)],
             db: Session = Depends(get_db)):
    return item_by_id(item_id=item_id, access_token=access_token, db=db)

@router.post("/create_item", response_model=schemas.LiteItem, status_code=201)
def create_update_item(access_token: Annotated[str, Depends(apikey_scheme)],
                       item_fields: schemas.ItemCreateUpdate,
                       item_data: UploadFile = File(...),
                       db: Session = Depends(get_db)):
    return item_add_update(access_token, db=db, item_fields=item_fields,
                           item_data=item_data)
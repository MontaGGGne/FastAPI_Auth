from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from typing import Annotated, List

from views.users import all_users, user_by_token
from models import schemas
from secure import apikey_scheme
from models.database import get_db
from controllers.users import register


router = APIRouter()

@router.get("/", response_model=List[schemas.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = all_users(db, skip=skip, limit=limit)
    return users

@router.post("", response_model=schemas.LiteUser, status_code=201)
def register_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    return register(db=db, user_data=user_data)

@router.get("/self", response_model=schemas.LiteUser)
def get_self_user(access_token: Annotated[str, Depends(apikey_scheme)], db: Session = Depends(get_db)):
    return user_by_token(access_token=access_token, db=db)
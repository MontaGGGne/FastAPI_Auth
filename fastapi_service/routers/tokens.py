from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from typing import List

from views.users import get_users
from models import schemas
from models.database import get_db
from controllers.tokens import create_token


router = APIRouter()

@router.post("", response_model=schemas.Token, status_code=201)
def create_token(user_data: schemas.UserAuth, db: Session = Depends(get_db)):
    return create_token(db=db, user_data=user_data)
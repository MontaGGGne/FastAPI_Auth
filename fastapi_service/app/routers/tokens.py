from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models import schemas
from app.models.database import get_db
from app.controllers.tokens import create_token


router = APIRouter()

@router.post("", response_model=schemas.Token, status_code=201)
def register_token(user_data: schemas.UserAuth, db: Session = Depends(get_db)):
    return create_token(db=db, user_data=user_data)
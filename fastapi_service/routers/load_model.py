from fastapi import APIRouter
from fastapi import HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from ml.model import load_autoencoder_model

from additional_methods.get_env import *


router = APIRouter()

@router.on_event("startup")
async def startup_event():
    try:
        global ml_model
        ml_model = load_autoencoder_model()
    except:
        ml_model = None
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Error load autoencoder model"
        )
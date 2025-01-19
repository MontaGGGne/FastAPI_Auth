from fastapi import FastAPI

from routers.items import router as items_router
from routers.users import router as users_router
from routers.tokens import router as tokens_router
from routers.load_model import router as load_model_router

from ml.model import load_autoencoder_model

from additional_methods.get_env import *


app = FastAPI()

# app.include_router(
#     router=load_model_router,
#     prefix='/load_model'
# )

app.include_router(
    router=items_router,
    prefix='/items'
)

app.include_router(
    router=users_router,
    prefix='/users'
)

app.include_router(
    router=tokens_router,
    prefix='/tokens'
)
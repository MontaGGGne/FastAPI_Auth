from fastapi import FastAPI
from fastapi import HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from routers.items import router as items_router
from routers.users import router as users_router
from routers.tokens import router as tokens_router

from ml.model import load_autoencoder_model



app = FastAPI()

# @app.on_event("startup")
# async def startup_event():
#     try:
#         ML_MODEL = load_autoencoder_model()
#     finally:
#         ML_MODEL = None
#         raise HTTPException(
#             status_code=HTTP_500_INTERNAL_SERVER_ERROR,
#             detail = "Error load autoencoder model"
#         )

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
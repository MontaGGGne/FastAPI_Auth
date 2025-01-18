from fastapi import FastAPI
from fastapi import HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from routers.items import router as items_router
from routers.users import router as users_router
from routers.tokens import router as tokens_router

from ml.model import load_autoencoder_model

from additional_methods.get_env import *
from s3.s3_conn import boto3_conn



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

@app.get("/upload") 
def upload():
    s3 = boto3_conn() 
    response = s3.generate_presigned_post( 
        Bucket=BUCKET_ID, 
        Key="file.txt" , 
        Conditions= None , 
        ExpiresIn= 3600
    )
    print(response["fields"])
    return {"url": response["url"], "fields": response["fields"]}

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
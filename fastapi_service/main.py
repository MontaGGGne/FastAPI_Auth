from typing import Union
from fastapi import FastAPI
from models import core
from models.database import engine
from routers.items import router as items_router
from routers.users import router as users_router


core.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(
    router=items_router,
    prefix='/items'
)

app.include_router(
    router=users_router,
    prefix='/users'
)
from fastapi import FastAPI

from app.routers.items import router as items_router
from app.routers.users import router as users_router
from app.routers.tokens import router as tokens_router


app = FastAPI()

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
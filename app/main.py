from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI

from app.api.routes.users import router as user_routers
from app.db.init_db import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    create_tables()
    yield


app = FastAPI(title="User Management API", lifespan=lifespan)

app.include_router(user_routers)

@app.get("/health")
def health_check():
    return {"status": "ok", "statusCode": 200}
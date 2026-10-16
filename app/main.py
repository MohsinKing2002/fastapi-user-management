from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI

from app.api.routes.users import router as user_routers
from app.db.init_db import create_tables


# lifespan event
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    create_tables()
    yield


# FastAPI application
app = FastAPI(title="User Management API", lifespan=lifespan)


# include routers
app.include_router(user_routers)


# health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok", "statusCode": 200}
from fastapi import FastAPI

from app.api.routes.users import router as user_routers
from app.core.config import get_settings

settings = get_settings()

# FastAPI application
app = FastAPI(title=settings.app_name, debug=settings.debug)


# include routers
app.include_router(user_routers)


# health check endpoint
@app.get("/health")
def health_check() -> dict[str, str]:
    """Health check endpoint"""

    return {"status": "ok", "statusCode": 200, "message": "Server is Healthy"}

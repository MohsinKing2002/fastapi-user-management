from fastapi import FastAPI

from app.api.routes.users import router as user_routers

# FastAPI application
app = FastAPI(title="User Management API")


# include routers
app.include_router(user_routers)


# health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok", "statusCode": 200}

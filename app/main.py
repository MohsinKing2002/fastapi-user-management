from fastapi import FastAPI
from app.db.session import engine

app = FastAPI(title="User Management API")

@app.get("/health")
def health_check():
    return {"status": "ok", "statusCode": 200}
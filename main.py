from fastapi import FastAPI

app = FastAPI(title="User Management API")


@app.get("/health")
def health_check():
    return {"status": "ok", "statusCode": 200}
from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/openapi.json"
)

@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}

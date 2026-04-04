from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routers import auth, users

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])

from app.api.routers import cms
app.include_router(cms.router, prefix="/api/v1/cms", tags=["cms"])

@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}

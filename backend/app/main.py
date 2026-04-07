from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.cache import init_cache, close_cache
from app.core.storage import init_storage, close_storage
from app.api.routers import auth, users, cms, webhooks


@asynccontextmanager
async def lifespan(app):
    await init_cache()
    await init_storage()
    yield
    await close_storage()
    await close_cache()


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/openapi.json",
    lifespan=lifespan,
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
app.include_router(cms.router, prefix="/api/v1/cms", tags=["cms"])
app.include_router(webhooks.router, prefix="/api/webhooks", tags=["webhooks"])


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}

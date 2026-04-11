
import json
import logging
import nh3
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import Response

logger = logging.getLogger(__name__)

class SafeCMSMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        if request.url.path.startswith("/api/v1/cms") and response.headers.get("content-type") == "application/json":
            body = b""
            async for chunk in response.body_iterator:
                body += chunk
            try:
                data = json.loads(body.decode("utf-8"))
                
                def sanitize(obj):
                    if isinstance(obj, dict):
                        return {k: sanitize(v) for k, v in obj.items()}
                    elif isinstance(obj, list):
                        return [sanitize(v) for v in obj]
                    elif isinstance(obj, str):
                        return nh3.clean(obj)
                    elif obj is None:
                        return ""
                    return obj
                
                safe_data = sanitize(data)
                body = json.dumps(safe_data).encode("utf-8")
                
                headers = dict(response.headers)
                if "content-length" in headers:
                    headers["content-length"] = str(len(body))
                return Response(content=body, status_code=response.status_code, headers=headers)
            except Exception:
                headers = dict(response.headers)
                return Response(content=body, status_code=response.status_code, headers=headers)
        return response

import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.cache import init_cache, close_cache
from app.core.storage import init_storage, close_storage
from app.api.routers import auth, users, cms, webhooks, files


@asynccontextmanager
async def lifespan(app):
    await init_cache()
    await init_storage()
    process = await asyncio.create_subprocess_exec(
        'python', 'seed_assets.py',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    yield
    if process.returncode is None:
        process.terminate()
        try:
            await asyncio.wait_for(process.wait(), timeout=5)
        except asyncio.TimeoutError:
            process.kill()
    await close_storage()
    await close_cache()


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/openapi.json",
    lifespan=lifespan,
)
app.add_middleware(SafeCMSMiddleware)

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
app.include_router(files.router, prefix="/api/v1/files", tags=["files"])


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}

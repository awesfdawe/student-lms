import re
from fastapi import APIRouter, Response, HTTPException
import httpx
import os
import redis

router = APIRouter()

redis_url = os.environ.get("REDIS_URL", "redis://127.0.0.1:6379")
try:
    r = redis.from_url(redis_url)
except Exception:
    r = None

directus_url = os.environ.get("DIRECTUS_URL", "http://127.0.0.1:8055")
email = os.environ.get("DIRECTUS_ADMIN_EMAIL", "admin@example.com")
password = os.environ.get("DIRECTUS_ADMIN_PASSWORD", "adminpassword")

SAFE_FILENAME = re.compile(r'^[a-zA-Z0-9_\-]+\.(svg|jpg|jpeg|png|webp|gif)$')

@router.get("/{filename}")
async def get_file(filename: str):
    if not SAFE_FILENAME.match(filename):
        raise HTTPException(status_code=400, detail="Invalid filename")

    cache_key = f"file_cache:{filename}"
    if r:
        try:
            cached = r.get(cache_key)
            if cached:
                content_type = "image/svg+xml" if filename.endswith(".svg") else "application/octet-stream"
                return Response(content=cached, media_type=content_type)
        except Exception:
            pass

    async with httpx.AsyncClient() as client:
        try:
            auth_res = await client.post(
                f"{directus_url}/auth/login",
                json={"email": email, "password": password}
            )
            headers = {}
            if auth_res.status_code == 200:
                token = auth_res.json().get("data", {}).get("access_token")
                if token:
                    headers["Authorization"] = f"Bearer {token}"

            search_res = await client.get(
                f"{directus_url}/files?filter[filename_download][_eq]={filename}",
                headers=headers
            )
        except Exception:
            raise HTTPException(status_code=500)
            
        if search_res.status_code != 200:
            raise HTTPException(status_code=404)
        
        data = search_res.json().get("data", [])
        if not data:
            raise HTTPException(status_code=404)
        
        file_id = data[0]["id"]
        file_res = await client.get(f"{directus_url}/assets/{file_id}", headers=headers)
        
        if file_res.status_code == 200:
            content = file_res.content
            content_type = file_res.headers.get("content-type", "application/octet-stream")
            
            if filename.endswith(".svg"):
                content_type = "image/svg+xml"
                
            if r:
                try:
                    r.setex(cache_key, 3600, content)
                except Exception:
                    pass
            return Response(content=content, media_type=content_type)
        raise HTTPException(status_code=404)

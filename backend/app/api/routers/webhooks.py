from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from app.core.cache import clear_cache
from app.core.config import settings
import os
import redis

router = APIRouter()

class WebhookPayload(BaseModel):
    collection: str
    event: str
    payload: dict

@router.post("/directus_update")
async def directus_update(
    webhook_data: WebhookPayload,
    x_webhook_secret: str = Header(None)
):
    expected_secret = getattr(settings, "WEBHOOK_SECRET", None)
    if expected_secret and x_webhook_secret != expected_secret:
        raise HTTPException(status_code=403)
    
    api_cleared = 0
    if webhook_data.collection == "directus_files":
        try:
            redis_url = os.environ.get("REDIS", "redis://redis:6379")
            r = redis.from_url(redis_url)
            keys = r.keys("file_cache:*")
            if keys:
                r.delete(*keys)
                api_cleared = len(keys)
        except Exception:
            pass
    else:
        api_cleared = await clear_cache(f"api_cache:/api/v1/cms/{webhook_data.collection}*")
        
    ssr_cleared = await clear_cache("ssr_page:*")
    
    return {
        "status": "success",
        "collection": webhook_data.collection,
        "keys_cleared": (api_cleared or 0) + (ssr_cleared or 0)
    }

from fastapi import APIRouter, Header, HTTPException
from app.core.config import settings
from app.core.cache import clear_cache, clear_all_cache
from app.schemas.webhook import DirectusPayload, WebhookResponse

router = APIRouter()


@router.post("/directus_update", response_model=WebhookResponse)
async def directus_update(
    body: DirectusPayload,
    x_webhook_secret: str = Header(default=""),
):
    if settings.WEBHOOK_SECRET and x_webhook_secret != settings.WEBHOOK_SECRET:
        raise HTTPException(status_code=403, detail="Invalid webhook secret")

    collection = body.collection
    if collection:
        deleted = await clear_cache(collection)
    else:
        deleted = await clear_all_cache()

    return {"status": "ok", "collection": collection, "keys_cleared": deleted}


from fastapi import APIRouter, Request
from app.core.cache import clear_cache
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/directus_update")
async def directus_update(request: Request):
    try:
        payload = await request.json()
        logger.info(f"Directus Hook Received: {payload.get('collection')} -> {payload.get('event')}")
        await clear_cache()
        return {"status": "ok", "message": "Cache invalidated"}
    except Exception as e:
        logger.error(f"Hook Error: {e}")
        return {"status": "error", "message": str(e)}

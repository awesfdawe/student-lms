import os
import httpx
import redis.asyncio as aioredis
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.database import get_db

router = APIRouter(prefix="/api/webhooks", tags=["webhooks"])

DIRECTUS_URL = os.getenv("DIRECTUS_URL", "http://directus:8055")
DIRECTUS_ADMIN_EMAIL = os.getenv("DIRECTUS_ADMIN_EMAIL", "admin@example.com")
DIRECTUS_ADMIN_PASSWORD = os.getenv("DIRECTUS_ADMIN_PASSWORD", "adminpassword")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

redis_client = aioredis.from_url(REDIS_URL, decode_responses=True)

async def get_directus_token():
    async with httpx.AsyncClient() as client:
        res = await client.post(f"{DIRECTUS_URL}/auth/login", json={
            "email": DIRECTUS_ADMIN_EMAIL,
            "password": DIRECTUS_ADMIN_PASSWORD
        })
        if res.status_code == 200:
            return res.json()["data"]["access_token"]
    return None

@router.post("/directus_update")
async def directus_update(request: Request, db: AsyncSession = Depends(get_db)):
    try:
        payload = await request.json()
    except Exception:
        return {"status": "error"}

    collection = payload.get("collection")
    keys = payload.get("keys", [])
    
    item = payload.get("item")
    if item and item not in keys:
        keys.append(item)

    if collection == "users" and keys:
        for key in keys:
            await redis_client.delete(f"user:{key}")
            
        token = await get_directus_token()
        if not token:
            return {"status": "error"}
            
        headers = {"Authorization": f"Bearer {token}"}
        
        async with httpx.AsyncClient() as client:
            roles_res = await client.get(f"{DIRECTUS_URL}/roles", headers=headers)
            roles_data = roles_res.json().get("data", [])
            admin_role_id = next((r["id"] for r in roles_data if r["name"] == "Administrator"), None)
            
            for key in keys:
                result = await db.execute(text("SELECT email, is_superuser FROM users WHERE id = :id"), {"id": key})
                user = result.fetchone()
                
                if not user:
                    continue
                    
                email, is_superuser = user
                
                d_users_res = await client.get(f"{DIRECTUS_URL}/users?filter[email][_eq]={email}", headers=headers)
                d_users = d_users_res.json().get("data", [])
                
                if is_superuser:
                    user_payload = {
                        "email": email,
                        "role": admin_role_id
                    }
                    if d_users:
                        await client.patch(f"{DIRECTUS_URL}/users/{d_users[0]['id']}", json=user_payload, headers=headers)
                    else:
                        await client.post(f"{DIRECTUS_URL}/users", json=user_payload, headers=headers)
                else:
                    if d_users:
                        await client.delete(f"{DIRECTUS_URL}/users/{d_users[0]['id']}", headers=headers)

    return {"status": "success"}

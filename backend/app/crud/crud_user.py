import os
import httpx
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserRegister
from app.core.security import get_password_hash

async def invalidate_directus_cache():
    try:
        directus_url = os.getenv("DIRECTUS_URL", "http://127.0.0.1:8055")
        email = os.getenv("DIRECTUS_ADMIN_EMAIL", "admin@example.com")
        password = os.getenv("DIRECTUS_ADMIN_PASSWORD", "adminpassword")
        
        async with httpx.AsyncClient() as client:
            res = await client.post(f"{directus_url}/auth/login", json={"email": email, "password": password})
            if res.status_code == 200:
                token = res.json()["data"]["access_token"]
                await client.post(
                    f"{directus_url}/utils/cache/clear",
                    headers={"Authorization": f"Bearer {token}"}
                )
    except Exception:
        pass

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()

async def create_user(db: AsyncSession, user_in: UserRegister) -> User:
    hashed_password = get_password_hash(user_in.password)
    db_user = User(
        email=user_in.email,
        hashed_password=hashed_password,
        is_active=True,
        is_superuser=False,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    await invalidate_directus_cache()
    
    return db_user

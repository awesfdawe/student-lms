from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.api.deps import get_db
from app.models.course import Course

router = APIRouter()

@router.get("/courses")
async def get_courses(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course))
    courses = result.scalars().all()
    return [{"id": c.id, "title": c.title, "slug": c.slug, "price": c.price} for c in courses]

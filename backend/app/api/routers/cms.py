from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.api.deps import get_db
from app.models.course import Course
from app.schemas.course import CourseRead
from app.core.cache import cache

router = APIRouter()


@router.get("/courses", response_model=list[CourseRead])
@cache(prefix="courses", ttl=300)
async def get_courses(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course))
    courses = result.scalars().all()
    return [{"id": c.id, "title": c.title, "slug": c.slug, "price": c.price} for c in courses]


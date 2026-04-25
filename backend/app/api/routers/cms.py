from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select
from app.core.database import get_db
from app.core.cache import cache
import logging
from app.models.quiz import Quiz
from app.schemas.quiz import QuizResponse

logger = logging.getLogger(__name__)
router = APIRouter()

SINGLETON_QUERIES = {
    "landing_page": text("SELECT * FROM landing_page LIMIT 1"),
    "globals": text("SELECT * FROM globals LIMIT 1"),
}

@router.get("/courses")
@cache(expire=3600)
async def get_courses(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT * FROM courses"))
    return [dict(r) for r in result.mappings().all()]

@router.get("/courses/{slug}")
@cache(expire=3600)
async def get_course(slug: str, request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT * FROM courses WHERE slug = :slug LIMIT 1"), {"slug": slug})
    row = result.mappings().first()
    if not row:
        raise HTTPException(status_code=404, detail="Course not found")
    return dict(row)

@router.get("/faqs")
@cache(expire=3600)
async def get_faqs(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT * FROM faqs"))
    return [dict(r) for r in result.mappings().all()]

@router.get("/quiz", response_model=list[QuizResponse])
@cache(expire=3600)
async def get_quiz(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Quiz).order_by(Quiz.id))
    return list(result.scalars().all())

@router.get("/ui_dictionary")
@cache(expire=3600)
async def get_ui_dictionary(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT * FROM ui_dictionary"))
    return [dict(r) for r in result.mappings().all()]

@router.get("/pages/{slug}")
@cache(expire=3600)
async def get_page(slug: str, request: Request, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(text("SELECT * FROM pages WHERE slug = :slug LIMIT 1"), {"slug": slug})
        row = result.mappings().first()
        if not row:
            raise HTTPException(status_code=404)
        return dict(row)
    except Exception as e:
        logger.error(f"DB Error getting page {slug}: {e}")
        raise HTTPException(status_code=404)

@router.get("/{collection_name}")
@cache(expire=3600)
async def get_singleton(collection_name: str, request: Request, db: AsyncSession = Depends(get_db)):
    query = SINGLETON_QUERIES.get(collection_name)
    if query is None:
        raise HTTPException(status_code=404)
    try:
        result = await db.execute(query)
        row = result.mappings().first()
        return dict(row) if row else {}
    except Exception as e:
        logger.error(f"DB Error getting singleton {collection_name}: {e}")
        return {}

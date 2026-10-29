from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from crud import news
from config.db_conf import get_db

router = APIRouter(prefix="/api/news", tags=["news"])

@router.get("/categories")
async def get_categories(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    categories = await news.get_categories(db, skip, limit)
    return {
        "code": 200,
        "message": "获取新闻分类成功",
        "data": categories
    }

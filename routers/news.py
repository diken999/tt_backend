from fastapi import APIRouter, Depends, Query, HTTPException
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

@router.get("/list")
async def get_news_list(
    category_id:  int = Query(..., alias="categoryId", description="新闻分类ID"),
    page: int = 1,
    page_size: int = Query(10, alias="pageSize", description="每页数量"),
    db: AsyncSession = Depends(get_db)
):
    offset = (page - 1) * page_size
    news_list = await news.get_news_list( db, category_id, offset, page_size)
    total = await news.get_news_count(db, category_id)
    has_more = offset + len(news_list) < total
    return {
        "code": 200,
        "message": "获取新闻列表成功",
        "data": {
            "list": news_list,
            "total": total,
            "has_more": has_more
        }
    }


@router.get("/detail")
async def get_news_detail(
    news_id: int = Query(..., alias="id", description="新闻 ID"),
    db: AsyncSession = Depends(get_db)
):
    news_detail = await news.get_news_detail(db, news_id)
    if not news_detail:
        raise HTTPException(status_code=404, detail="新闻未找到")

    increase_status = await news.increase_news_views(db, news_id)
    if not increase_status:
        raise HTTPException(status_code=404, detail="更新浏览量失败")

    related_news = await news.get_related_news(db, news_detail.id, news_detail.category_id, limit=5)
    return {
        "code": 200,
        "message": "获取新闻详情成功",
        "data": {
            "id": news_detail.id,
            "title": news_detail.title,
            "content": news_detail.content,
            "image": news_detail.image,
            "author": news_detail.author,
            "publishTime": news_detail.publish_time,
            "categoryId": news_detail.category_id,
            "views": news_detail.views,
            "relatedNews": related_news
        }
    }

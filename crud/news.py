from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession
from models.news import Categories, News

async def get_categories(db: AsyncSession ,skip: int = 0, limit: int = 10):
    stmt = select(Categories).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_news_list(db: AsyncSession, category_id: int, skip: int = 0, limit: int = 10):
    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_news_count(db: AsyncSession, category_id: int):
    # 查询指定分类的新闻总数
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one() # 返回单个结果，如果没有结果则抛出异常

async def get_news_detail(db: AsyncSession, news_id: int):
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()  # 返回单个结果，如果没有结果则返回 None

async def increase_news_views(db: AsyncSession, news_id: int):
    stmt = update(News).where(News.id == news_id).values(views=News.views + 1)
    result = await db.execute(stmt)
    await db.commit()

    # 更新 -> 检查数据库是否真的命中了数据
    return result.rowcount > 0  # 返回受影响的行数，如果为 0 则表示没有更新任何行

async def get_related_news(db: AsyncSession, news_id: int, category_id: int, limit: int = 5):
    # order_by 排序 => 浏览量和发布时间
    stmt = select(News).where(
        News.category_id == category_id,
        News.id != news_id
    ).order_by(
        News.views.desc(),
        News.publish_time.desc()
    ).limit(limit)
    result = await db.execute(stmt)
    # return result.scalars().all()
    related_news = result.scalars().all()
    return list(map(lambda news: {
        "id": news.id,
        "title": news.title,
        "image": news.image,
        # "author": news.author,
        # "publishTime": news.publish_time,
        # "views": news.views
    }, related_news))


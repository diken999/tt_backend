from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.news import Categories

async def get_categories(db: AsyncSession ,skip: int = 0, limit: int = 10):
    stmt = select(Categories).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

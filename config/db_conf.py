from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

ASYNC_DATABASE_URL = "mysql+asyncmy://root:12345678@localhost:3306/toutiao_news"

# 创建异步引擎
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,
    pool_size=5,
    max_overflow=10
)

# 创建异步会话工厂
async_session = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False  # 提交后不使对象属性过期，保持数据可访问
)

# 依赖项，用于获取数据库会话
async def get_db():
    async with async_session() as session:
        try:
            yield session  # 将会话对象产出给调用者，暂停函数执行直到请求结束
            await session.commit()  # 如果无异常，提交事务
        except Exception:
            await session.rollback()  # 发生异常时回滚事务
            raise  # 重新抛出异常以便上层处理
        finally:
            await session.close()  # 关闭会话，释放资源


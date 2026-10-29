from fastapi import FastAPI
from routers import news

app = FastAPI(title="头条后端接口", version="1.0.0")
# 注册路由
app.include_router(news.router)

@app.get("/")
async def read_root() -> dict[str, str]:
    return {"message": "Toutiao Backend API"}

# uv run uvicorn main:app --reload
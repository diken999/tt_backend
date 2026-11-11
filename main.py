from fastapi import FastAPI
from routers import news, users
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="头条后端接口", version="1.0.0")

# 允许的来源
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许的源
    allow_credentials=True, # 允许携带 cookie
    allow_methods=["*"], # 允许的请求方法
    allow_headers=["*"] # 允许的请求头
)
# 注册路由
app.include_router(news.router)
app.include_router(users.router)

@app.get("/")
async def read_root() -> dict[str, str]:
    return {"message": "Toutiao Backend API"}

# uv run uvicorn main:app --reload

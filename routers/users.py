from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from schemas.users import UserRegisterRequest
from crud.users import get_user_by_username, create_user

router = APIRouter(prefix="/api/user", tags=["users"])

@router.post("/register")
async def register_user(user_data: UserRegisterRequest, db: AsyncSession = Depends(get_db)):
    existing_user = await get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    user = await create_user(db, user_data)
    return {
        "code": 200,
        "message": "注册成功",
        "data": {
            "token": "123",
            "userInfo": {
                "id": user.id,
                "username": user.username,
                "bio": user.bio
            }
        }
    }

from starlette import status
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator
from fastapi import Depends, Request, HTTPException
from sqlalchemy import select

from app.models import User
from app.middleware.sessions import get_session_user, clear_session_user
from app.core.db_users import SessionUsers


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionUsers() as session:
        yield session

# Получаем текущего пользователя из сессии
async def get_current_user(request: Request) -> User | None:
    user_id = get_session_user(request)
    if not user_id:
        return None
    async with SessionUsers() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            clear_session_user(request)  # 👈 сбрасываем сессию, если пользователь не найден
            return None
        return user

# Получаем индивидуальную сессию для пользователя
async def get_user_db(user: User = Depends(get_current_user)) -> AsyncGenerator[AsyncSession, None]:
    if user is None:
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, headers={"Location": "/"})
    engine = create_async_engine(f"sqlite+aiosqlite:///{user.db_filename}", echo=True)
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with SessionLocal() as session:
        yield session

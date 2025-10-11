from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.settings import settings


UserBase = declarative_base()

engine_users = create_async_engine(settings.USER_DB_URL, echo=True)
SessionUsers = async_sessionmaker(engine_users, class_=AsyncSession, expire_on_commit=False)
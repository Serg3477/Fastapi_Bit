from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.core.settings import settings

HistoryBase = declarative_base()

engine_history = create_async_engine(settings.HISTORY_DB_URL, echo=True)
SessionHistory = async_sessionmaker(engine_history, class_=AsyncSession, expire_on_commit=False)

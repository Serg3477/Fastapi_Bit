from app.core.db_users import engine_users, UserBase
from sqlalchemy import create_engine
from app.core.settings import settings
from app.core.db_history import HistoryBase

async def init_db():
    async with engine_users.begin() as conn:
        await conn.run_sync(UserBase.metadata.create_all)

def create_history_database():
    engine = create_engine(settings.HISTORY_DB_URL.replace("sqlite+aiosqlite", "sqlite"))
    HistoryBase.metadata.create_all(engine)

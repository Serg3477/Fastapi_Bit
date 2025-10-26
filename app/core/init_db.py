from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.db_users import engine_users, UserBase
from app.core.db_history import engine_history, HistoryBase
from app.core.db_tenant import TenantBase
from app.core.settings import settings

# users.db
async def create_user_database():
    async with engine_users.begin() as conn:
        await conn.run_sync(UserBase.metadata.create_all)

# history.db
async def create_history_database():
    async with engine_history.begin() as conn:
        await conn.run_sync(HistoryBase.metadata.create_all)

# tenant-базы
def create_tenant_database(db_path: str):
    engine = create_engine(f"sqlite:///{db_path}")
    TenantBase.metadata.create_all(engine)

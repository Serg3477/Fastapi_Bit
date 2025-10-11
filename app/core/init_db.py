from app.core.db_users import engine_users, UserBase

async def init_db():
    async with engine_users.begin() as conn:
        await conn.run_sync(UserBase.metadata.create_all)


from datetime import datetime
from app.models import UserLog  # 👈 модель для истории
from sqlalchemy.ext.asyncio import AsyncSession

async def log_event(db: AsyncSession, user_id: int, action: str, details: str = ""):
    log = UserLog(
        user_id=user_id,
        action=action,
        details=details,
        timestamp=datetime.utcnow()
    )
    db.add(log)
    await db.commit()
